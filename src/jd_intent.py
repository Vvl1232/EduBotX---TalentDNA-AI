class JDIntentExtractor:

    def __init__(self):
        pass

    def extract(self, jd_text):

        text = jd_text.lower()

        intent = {

            "needs_retrieval": False,
            "needs_ranking": False,
            "needs_llm": False,
            "needs_evaluation": False,
            "needs_production_ml": False,
            "needs_product_experience": False
        }

        if "retrieval" in text:
            intent["needs_retrieval"] = True

        if "ranking" in text:
            intent["needs_ranking"] = True

        if (
            "llm" in text or
            "fine-tuning" in text
        ):
            intent["needs_llm"] = True

        if (
            "ndcg" in text or
            "mrr" in text or
            "map" in text
        ):
            intent["needs_evaluation"] = True

        if (
            "production" in text or
            "deployed" in text
        ):
            intent["needs_production_ml"] = True

        if (
            "product company" in text or
            "product companies" in text
        ):
            intent["needs_product_experience"] = True

        return intent