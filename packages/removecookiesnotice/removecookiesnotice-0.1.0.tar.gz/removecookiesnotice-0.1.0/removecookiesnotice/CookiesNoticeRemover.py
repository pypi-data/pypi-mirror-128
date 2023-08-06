import lxml.html
import logging
from functools import total_ordering
import sys
import re

ATTRIBUTES_PATTERNS = [
    "cookie",
    "notice",
    "qc",
    "didomi",
    "consent",
    "cybot",
    "policy",
    "privacy",
    "advert",
    "popup",
    "advert",
    "alert",
    "dismiss",
    "banner",
    "modal",
    "directive",
    "notification",
    "cnil",
    "cc",
    "page",
    "disclaimer",
    "content",
]

ATTRIBUTES_LIST = ["id", "class", "data-cookie-banner", "data-testid"]

TEXT_PATTERNS = [
    "cookie",
    "j'accepte",
    "conditions générales",
    "contenu personnalisé",
    "nos partenaires",
    "informations personnelles",
    "analyser l'audience",
    "campagnes de publicité ciblées",
    "configuration des cookies",
    "personnaliser le contenu",
    "politique de confidentialité",
    "publicités",
    "politique d’utilisation des cookies",
    "vous nous autorisez à collecter des informations",
    "consent to our use of cookies",
    "cookie policy",
    "meilleure expérience",
    "optimiser votre expérience",
    "adapter la publicité",
    "consentez à l’utilisation de ces cookies",
    "publicités personnalisée",
    "vous acceptez leur utilisation",
    "politique relative aux cookies",
    "statistiques de visites",
    "proposer",
    "services",
    "offres",
    "publicités",
    "partenaires tiers",
    "centres d’intérêt",
    "centre d’intérêt",
    "utilisation de cookies",
    "personnaliser votre expérience",
    "analyser notre trafic",
    "partageons des informations",
    "partenaires",
    "médias sociaux",
    "publicité",
    "analyse",
    "traitements de données",
    "accéder à des informations sur votre appareil",
]

TO_KEEP_TAGS = ["body"]

logger = logging.getLogger("CookiesNoticeRemover")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


@total_ordering
class ToRemoveTag:
    def __init__(self, lxml_element, weight: int):
        self.lxml_element = lxml_element
        self.tag = lxml_element.tag.lower()
        self.weight = weight
        self.attributes = lxml_element.attrib

    def __eq__(self, other):
        if not isinstance(other, ToRemoveTag):
            return False

        return self.lxml_element == other.lxml_element

    def __neq__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, ToRemoveTag):
            return True

        return self.weight < other.weight

    def __repr__(self):
        return f"{self.tag} with weight {self.weight} and attributes {self.attributes}"


class CookiesNoticeRemover:
    def __init__(
        self,
        minimum_attribute_hints=2,
        minimum_density=0.1,
        no_childrens_evidence_treshold=2,
        verbose=False,
    ):
        self.__attribute_patterns_set = {
            attribute_pattern.lower()
            for attribute_pattern in ATTRIBUTES_PATTERNS
        }
        self.__text_patterns = sorted(
            TEXT_PATTERNS, key=lambda t: len(t), reverse=True
        )

        self.__logger = None
        if verbose:
            self.__logger = logger

        self.__minimum_attribute_hints = minimum_attribute_hints
        self.__minimum_density = minimum_density
        self.__no_childrens_evidence_treshold = no_childrens_evidence_treshold

    def remove(self, content):
        tree = lxml.html.fromstring(content)

        attribute_matching_elements = self.__search_attribute_patterns(tree)
        self.__write_log(
            f"Will remove {attribute_matching_elements} attribute matching elements"
        )
        self.__remove_matching_elements(attribute_matching_elements)

        text_matching_elements = self.__search_text_patterns(
            tree, self.__minimum_density
        )
        self.__write_log(
            f"Will remove {text_matching_elements} text matching elements"
        )
        self.__remove_matching_elements(text_matching_elements)

        return lxml.html.tostring(tree, pretty_print=True)

    def __search_attribute_patterns(self, element):
        return self.__search_attribute_patterns_acc(element, [])

    def __search_attribute_patterns_acc(self, element, matching_elements):
        element_attributes = self.__get_element_attributes(element)
        attributes_found_hints = self.__compute_attributes_hints(
            element_attributes
        )
        matching_attributes = [
            attribute
            for attribute, nb_hints in attributes_found_hints.items()
            if nb_hints >= self.__minimum_attribute_hints
        ]

        if len(matching_attributes) > 0:
            matching_elements.append(
                ToRemoveTag(
                    element, 1
                )  # Attributes matched elements all have same weight
            )
            return matching_elements
        else:
            for child in element:
                self.__search_attribute_patterns_acc(child, matching_elements)
            return matching_elements

    def __get_element_attributes(self, element):
        return {
            attribute_value.lower()
            for attribute_name, attribute_string_value in element.attrib.items()
            for attribute_value in attribute_string_value.split(" ")
            if attribute_name.lower() in ATTRIBUTES_LIST
        }

    def __compute_attributes_hints(self, element_attributes):
        attributes_found_hints = {
            attribute: 0 for attribute in element_attributes
        }
        for attribute_hint in self.__attribute_patterns_set:
            for element_attribute in element_attributes:
                if attribute_hint in element_attribute:
                    attributes_found_hints[element_attribute] += 1

        return attributes_found_hints

    def __remove_matching_elements(self, elements):
        sorted_elements = sorted(elements, reverse=True)
        for element in sorted_elements:
            self.__remove_matching_element(element)

    def __remove_matching_element(self, element):
        if element.tag not in TO_KEEP_TAGS:
            element.lxml_element.getparent().remove(element.lxml_element)
        else:
            self.__write_log("Will not remove element because in TO_KEEP_TAGS")

    def __search_text_patterns(self, element, minimum_density):
        return self.__search_text_patterns_acc(element, [], minimum_density)

    def __search_text_patterns_acc(
        self, element, matching_elements, minimum_density
    ):
        matching_text_patterns = self.__search_matching_text_patterns(element)
        matched_density = self.__compute_matched_density(
            element, matching_text_patterns
        )

        if len(matching_text_patterns) == 0:
            # Optimisation to cut empty tree branches
            return matching_elements
        elif matched_density >= minimum_density:
            # Matched text is dense enough for removal
            matching_elements.append(
                ToRemoveTag(element, len(matching_text_patterns))
            )
            return matching_elements
        elif (
            len(element) == 0
            and len(matching_text_patterns)
            > self.__no_childrens_evidence_treshold
        ):
            # Element with no child is not dense enough
            # But it has enough pattern to be sure
            matching_elements.append(
                ToRemoveTag(element, len(matching_text_patterns))
            )
            return matching_elements
        else:
            # Matched text is not dense enough
            # Continue searching dense enough regions in childrens
            for child in element:
                self.__search_text_patterns_acc(
                    child, matching_elements, minimum_density
                )
            return matching_elements

    def __search_matching_text_patterns(self, element):
        text = self.__get_element_text(element)

        detected_patterns = []
        for pattern in self.__text_patterns:
            regex_pattern = f".*{pattern}.*"
            match = re.match(regex_pattern, text, re.IGNORECASE)
            if match:
                detected_patterns.append(pattern)
                text = re.sub(pattern, " ", text, flags=re.IGNORECASE)

        return detected_patterns

    def __compute_matched_density(self, element, matching_text_patterns):
        """Compute density by text coverage.

        Density = (text_covered_by_patterns) / total_length

        """
        text_length = len(self.__get_element_text(element))

        if text_length == 0:
            return 0

        total_matched_length = sum(
            [len(pattern) for pattern in matching_text_patterns]
        )

        return total_matched_length / text_length

    def __get_element_text(self, element):
        """Clean an lxml element text."""
        try:
            text = element.text_content()
            text = re.sub("\t", " ", text)
            text = re.sub("\r", " ", text)
            text = re.sub(" ?\n ?", "\n", text)
            text = re.sub("\n{2,}", "\n", text)
            text = re.sub("\n", ". ", text)
            text = re.sub(r"\.+", ".", text)
            text = re.sub(
                r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", "", text
            )  # Removes emails
            text = re.sub(
                r"([a-zA-Z0-9_.+-]+ ?\[ ?a ?\] ?[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
                "",
                text,
            )  # Remove obfuscated emails
            text = re.sub(
                r"(http[s]?://)?([A-Z0-9a-z]+\.)+[A-Z0-9a-z]{1,6}", "", text,
            )  # Remove urls
            text = re.sub(" +", " ", text)
            text = text.strip()

            return text
        except Exception:
            return ""

    def __write_log(self, message):
        if self.__logger is not None:
            self.__logger.info(message)
