"""
TalentDNA AI - jd_parser Module used for converting raw job descriptionn to JSON K-V pair
"""

import re


class JDParser:

    def __init__(self):
        pass

    def extract_experience(self, jd_text):

        match = re.search(
            r'(\d+)\s*-\s*(\d+)\s*years',
            jd_text.lower()
        )

        if match:

            return {
                "min_exp": int(match.group(1)),
                "max_exp": int(match.group(2))
            }

        return {
            "min_exp": 0,
            "max_exp": 100
        }

    def extract_role(self, jd_text):

        first_line = jd_text.split("\n")[0]

        return first_line.strip()

    def build_jd_text(self, jd_text):

        return jd_text

    def parse(self, jd_text):

        return {

            "role":
                self.extract_role(
                    jd_text
                ),

            **self.extract_experience(
                jd_text
            ),

            "jd_text":
                self.build_jd_text(
                    jd_text
                )
        }