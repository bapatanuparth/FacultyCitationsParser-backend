import re
import spacy
from elite_journals import elite_journals


# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Adjusted regex pattern
# author_pattern = re.compile(r'([A-Za-z]+,?\s[A-Z]\.(?:\s[A-Z]\.)?)')
# author_pattern = re.compile(r'([A-Za-z]+,?\s[A-Z]\.(?:\s?[A-Z]\.)?)')
author_pattern = re.compile(r'([A-Za-z]+,?\s[A-Z][.,](?:\s?[A-Z][.,])?)')

# author_pattern = re.compile(r'([A-Za-z]+, [A-Z]\.([A-Z]\.)?)')

citations = [
    # "*Mu, S. & Gnyawali, D. R. 2005. “Exploration Exploitation: The Effects of Subsidiary Learning Strategy on Knowledge Outcomes.” Annual Meeting of the Academy of Management, Honolulu, HI.",
    # "1.	Awate K. Makhija M., A Trojan Horse inside the gates? Knowledge spillovers during patent litigation. Academy of Management Journal 65, no. 5 (2022): 1747-1769",
    # "2.	Awate K., Makhija M., Xiao T. A Puzzle of Knowledge Spillovers to During Patent Litigation Academy of Management Perspectives. In-press",
    # "Gnyawali, D. R. Co-opetition between Giants: Drivers and Consequences of Collaboration between Large Competitors.” Research Policy, 40: 650-663.",
    # "Gnyawali, D. R. *Offstein, E. H., Lau, R. 2008. “The Impact of the CEO Pay Gap on Firm Competitive Behavior.” Group & Organization Management, 33: 453-484.",
    # "Haynes, K.T, Tihanyi, L.K, A 21 country ",
    # "Steinbach, A, Holmes, R.M, Holcomb, T.R., Devers, C.E. & Cannella, A.A. (2017) Top manager incentive heterogeneity, strategic investment behavior, and performance: A social psychological theory of incentive alignment, Strategic Management Journal, 38: 1701-1720.",
"Czakon, W. *Srivastava, M.K., Le Roy, F. Gnyawali, D.R. 2020. Coopetition Strategies: Critical Issues and Research Directions. Long Range Planning, volume 53 (1) hal-02517434.",
"Rai, R., Gnyawali, D.R., & Bhatt, H. 2023. Walking the Tightrope: Coopetition Capability Construct and its Role in Value Creation. Journal of Management, 49, 7: 2354-2386.",
"Gnyawali, D.R. “Managing Interdependence in Strategic Alliances”. Presented at a Symposium at the 2023 International Conference of the Strategic Management Society, Toronto, Canada.",
"Roehrich, J., Squire, B., Taubeneder, R., Tyler, B., & Gnyawali, D.R. 2023. “Managing Coopetition in a Multiparty Supplier Alliance”. 2023 Academy of Management Conference, Boston."
]


journal_id=["Academy", "Management", "Planning", "Organization","Business","strategic","review","Meeting","Organizational","of","the","and","journal",
            "Development","Finance", "Operations","Annual","Proceedings","Acquisitions","research","International","Corporate","Quarterly","Conference",
            "Society","Symposium","Technological","Strategy","Entrepreneurship","Strategies"]

def extract_journal(remaining_text):
    substrings = re.split(r'[,.?]\s*', remaining_text)
    # Convert journal_id to lowercase for case-insensitive comparison
    journal_id_lower = [x.lower() for x in journal_id]
    
    # Iterate over substrings from the end
    for substring in reversed(substrings):
        # Split substring into words and convert to lowercase for case-insensitive comparison
        words = substring.lower().split()
        # Check if any word in substring is in journal_id
        if any(word in journal_id_lower for word in words):
            start_index = remaining_text.lower().rfind(substring.lower())
            return substring, start_index  # Return the original case substring
    return remaining_text, -1

def check_elite_journal(citation, elite_journals):
    citation_lower = citation.lower()
    for journal in elite_journals:
        if journal.lower() in citation_lower:
            return journal
    return None

def extract_year(input_string):
    # Pattern to find a year in the range of 1900 to 2099
    year_pattern = r'\b(19|20)\d{2}\b'
    
    match = re.search(year_pattern, input_string)
    
    if match:
        year = match.group()  # The matched year
        # Remove the first occurrence of the matched year from the input string
        remaining_string = re.sub(year, '', input_string, count=1).strip()
        return year, remaining_string
    else:
        return None, input_string

def clean_string(input_string):
    # Regular expression to match punctuation at the start and end of the string
    # ^[\W_]+ matches punctuation at the start of the string
    # [\W_]+$ matches punctuation at the end of the string
    cleaned_string = re.sub(r'^[\W_]+|[\W_]+$', '', input_string)
    return cleaned_string

def process_citation(citations):
    extracted_data = []
    for citation in citations:

        ############ Check if elite journal ########
        elite_journal=check_elite_journal(citation, elite_journals)

        ########Extract authors#############
        authors = author_pattern.findall(citation)
        matches = list(re.finditer(author_pattern, citation))
        print(f"Citation: {citation}")
        print(f"Extracted Authors: {authors}")

        ########## Extract the remaining string for further processing #####################
        if matches:
            last_match = matches[-1]  # Get the last match object
            last_index = last_match.end()  # Get the end position of the last match
            
            remaining_text = citation[last_index:]
            year, remaining_string = extract_year(remaining_text)
            journal_name, start_index = extract_journal(remaining_string)
            if start_index == -1:
                paper_title = remaining_string.strip()  # Use the whole remaining_text as the paper title
            else:
        # Extract the paper title from the beginning of `remaining_text` up to `start_index`
                paper_title = remaining_string[:start_index].strip()
            journal_name=clean_string(journal_name)
            paper_title=clean_string(paper_title)
            # print(f"Remaining Text: {remaining_string}")
            print(f"Journal Name: {journal_name}")
            print(f"Paper Title: {paper_title}")
            print(f"Years Extracted: {year}\n")
            print(f"Elite Journal: {elite_journal}\n")
            citation_data = {
                "citation":citation,
                "authors": authors,
                "journal_name": journal_name,
                "paper_title": paper_title,
                "year": year,
                "elite_journal": elite_journal
            }
            extracted_data.append(citation_data)
    return extracted_data
