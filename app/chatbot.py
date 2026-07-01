"""
chatbot.py

Main conversational agent for the SHL Assessment Recommender.
"""

import logging
from typing import Dict, List

from app.conversation import (
    extract_state,
    clarification_question,
    need_clarification,
)

from app.guardrails import (
    is_off_topic,
    refusal_message,
)

from app.llm import generate

from app.prompts import (
    SYSTEM_PROMPT,
    RECOMMENDATION_PROMPT,
    COMPARISON_PROMPT,
)

from app.retriever import retriever


logger = logging.getLogger(__name__)


class SHLChatbot:
    """
    Main orchestrator.

    Responsibilities
    ----------------
    - Understand conversation
    - Ask clarification questions
    - Retrieve assessments
    - Compare assessments
    - Generate grounded responses
    """

    def __init__(self):

        self.retriever = retriever

    # ============================================================
    # PUBLIC ENTRY POINT
    # ============================================================

    def chat(self, messages: List[Dict]) -> Dict:

        logger.info("New chat request received.")

        if not messages:

            return {
                "reply": "How can I help you choose an SHL assessment today?",
                "recommendations": [],
                "end_of_conversation": False,
            }

        user_message = self._latest_user_message(messages)

        logger.info(f"Latest user message: {user_message}")

        # ----------------------------------------------------
        # Guardrails
        # ----------------------------------------------------

        if is_off_topic(user_message):

            logger.info("Off-topic request detected.")

            return {
                "reply": refusal_message(),
                "recommendations": [],
                "end_of_conversation": False,
            }

        # ----------------------------------------------------
        # Extract conversation state
        # ----------------------------------------------------

        state = extract_state(messages)

        state["messages"] = messages

        if "skills" not in state:
            state["skills"] = []

        logger.info(f"Conversation state: {state}")

        # ----------------------------------------------------
        # Need clarification?
        # ----------------------------------------------------

        if need_clarification(state):

            logger.info("Clarification required.")

            return {
                "reply": clarification_question(state),
                "recommendations": [],
                "end_of_conversation": False,
            }

        # ----------------------------------------------------
        # Comparison Flow
        # ----------------------------------------------------

        if state.get("comparison"):

            logger.info("Comparison request detected.")

            return self.compare(state)

        # ----------------------------------------------------
        # Recommendation Flow
        # ----------------------------------------------------

        logger.info("Recommendation flow.")

        return self.recommend(state)
    
    # ============================================================
    # RECOMMENDATION FLOW
    # ============================================================

    def recommend(self, state: Dict) -> Dict:
        """
        Retrieve the most relevant SHL assessments
        and generate a grounded recommendation.
        """

        # ----------------------------------------------------
        # Build Retrieval Query
        # ----------------------------------------------------

        query_parts = []

        if state.get("role"):
            query_parts.append(state["role"])

        if state.get("seniority"):
            query_parts.append(state["seniority"])

        if state.get("personality"):
            query_parts.append("personality")

        if state.get("skills"):
            query_parts.extend(state["skills"])

        query = " ".join(query_parts).strip()

        if not query:
            query = self._latest_user_message(state["messages"])

        logger.info(f"Retrieval Query: {query}")

        # ----------------------------------------------------
        # Retrieve Documents
        # ----------------------------------------------------

        try:

           results = self._filter_results(
           self.retriever.search(
           query=query,
           top_k=5,
    )
)
        except Exception as e:

            logger.exception(e)

            return {
                "reply": (
                    "An error occurred while searching the SHL "
                    "assessment catalog."
                ),
                "recommendations": [],
                "end_of_conversation": False,
            }

        if len(results) == 0:

            return {
                "reply": (
                    "I couldn't find suitable SHL assessments "
                    "matching your requirements."
                ),
                "recommendations": [],
                "end_of_conversation": False,
            }

        # ----------------------------------------------------
        # Build Context
        # ----------------------------------------------------

        context = self._build_context(results)

        logger.info("Retrieved %d assessments", len(results))

        # ----------------------------------------------------
        # Build Prompt
        # ----------------------------------------------------

        prompt = (
            SYSTEM_PROMPT
            + "\n\n"
            + RECOMMENDATION_PROMPT.format(
                query=query,
                context=context,
            )
        )

        # ----------------------------------------------------
        # Generate Response
        # ----------------------------------------------------

        try:

            reply = generate(prompt)

        except Exception as e:

            logger.exception(e)

            reply = (
                "Based on your requirements, I found the following "
                "SHL assessments."
            )

        # ----------------------------------------------------
        # Format Recommendations
        # ----------------------------------------------------

        recommendations = self._format_recommendations(results)

        logger.info(
            "Returning %d recommendations",
            len(recommendations),
        )

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": True,
        }
    
    # ============================================================
    # COMPARISON FLOW
    # ============================================================

    def compare(self, state: Dict) -> Dict:
        """
        Compare two SHL assessments using retrieved catalog data.
        """

        names = state.get("compare_names", [])

        if len(names) < 2:
            return {
                "reply": (
                    "Please specify the two SHL assessments you "
                    "would like to compare."
                ),
                "recommendations": [],
                "end_of_conversation": False,
            }

        logger.info("Comparing: %s vs %s", names[0], names[1])

        try:

            first = self.retriever.search(
                query=names[0],
                top_k=1,
            )

            second = self.retriever.search(
                query=names[1],
                top_k=1,
            )

        except Exception as e:

            logger.exception(e)

            return {
                "reply": (
                    "An error occurred while retrieving the "
                    "requested assessments."
                ),
                "recommendations": [],
                "end_of_conversation": False,
            }

        if not first or not second:

            return {
                "reply": (
                    "I couldn't locate one or both assessments "
                    "in the SHL catalog."
                ),
                "recommendations": [],
                "end_of_conversation": False,
            }

        assessment1 = first[0]
        assessment2 = second[0]

        prompt = (
            SYSTEM_PROMPT
            + "\n\n"
            + COMPARISON_PROMPT.format(
                assessment1=assessment1["text"],
                assessment2=assessment2["text"],
            )
        )

        try:

            reply = generate(prompt)

        except Exception as e:

            logger.exception(e)

            reply = (
                f"Comparison between "
                f"{assessment1['name']} and "
                f"{assessment2['name']} "
                f"could not be generated."
            )

        return {
            "reply": reply,
            "recommendations": [],
            "end_of_conversation": False,
        }
    
    # ============================================================
    # HELPER FUNCTIONS
    # ============================================================

    def _latest_user_message(self, messages: List[Dict]) -> str:
        """
        Return the latest user message from the conversation.
        """

        for message in reversed(messages):

            if message["role"] == "user":
                return message["content"]

        return ""

    def _build_context(self, results: List[Dict]) -> str:
        """
        Convert retrieved assessments into LLM context.
        """

        chunks = []

        for item in results:

            chunks.append(item["text"])

        return "\n\n".join(chunks)

    def _format_recommendations(
        self,
        results: List[Dict],
    ) -> List[Dict]:
        """
        Convert retrieval results into API response format.
        """

        recommendations = []

        for item in results:

            recommendations.append(
                {
                    "name": item["name"],
                    "url": item["url"],
                    "test_type": ", ".join(
                        item.get("keys", [])
                    ),
                }
            )

        return recommendations

    def _filter_results(
        self,
        results: List[Dict],
        threshold: float = 0.40,
    ) -> List[Dict]:
        """
        Remove low-confidence retrievals.
        """

        filtered = []

        for item in results:

            if item.get("score", 0.0) >= threshold:
                filtered.append(item)

        return filtered


# ============================================================
# Singleton
# ============================================================

chatbot = SHLChatbot()