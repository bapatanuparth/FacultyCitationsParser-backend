import pandas as pd

def json_to_excel(data, output_path):
    # Define the structure of our DataFrame for each category
    columns = ['Name', 'citation', 'authors', 'year', 'paper_title', 'journal_name']
    
    # Initialize empty DataFrames for each category
    publications_df = pd.DataFrame(columns=columns)
    conferences_df = pd.DataFrame(columns=columns)
    book_chapters_df = pd.DataFrame(columns=columns)
    elite_publications_df = pd.DataFrame(columns=columns)
    
    # Loop through each person in the data
    for person in data:
        name = person['name']
        
        # Helper function to append rows to our DataFrames
        def append_items(items, df):
            temp_elite_df = pd.DataFrame(columns=columns) 
            for item in items:
                row = {
                    'Name': name,
                    'citation': item.get('citation', ''),
                    'authors': ', '.join(item.get('authors', [])),
                    'year': item.get('year', ''),
                    'paper_title': item.get('paper_title', ''),
                    'journal_name': item.get('journal_name', '')
                }
                df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
                if item.get('elite_journal') != "":
                    # global elite_publications_df
                    temp_elite_df = pd.concat([temp_elite_df, pd.DataFrame([row])], ignore_index=True)
            return df, temp_elite_df
        
        # Append data to each DataFrame
        publications_df,temp_elite_df = append_items(person['publications'], publications_df)
        elite_publications_df = pd.concat([elite_publications_df, temp_elite_df], ignore_index=True)
        conferences_df,temp_elite_df = append_items(person['conferences'], conferences_df)
        elite_publications_df = pd.concat([elite_publications_df, temp_elite_df], ignore_index=True)
        book_chapters_df,temp_elite_df = append_items(person['bookChapters'], book_chapters_df)
        elite_publications_df = pd.concat([elite_publications_df, temp_elite_df], ignore_index=True)
    
    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(output_path, engine='openpyxl')
    
    # Write each DataFrame to a specific sheet
    publications_df.to_excel(writer, sheet_name='Publications', index=False)
    conferences_df.to_excel(writer, sheet_name='Conferences', index=False)
    book_chapters_df.to_excel(writer, sheet_name='Book Chapters', index=False)
    elite_publications_df.to_excel(writer, sheet_name='Elite Publications', index=False)
    
    # Close the Pandas Excel writer and save the Excel file to disk
    writer.save()

# Sample data
data = [
    {
        "bookChapters": [],
        "conferences": [],
        "name": "Christopher Courtney",
        "publications": []
    },
    {
        "bookChapters": [],
        "conferences": [
            {
                "authors": [
                    "Yonish, L.",
                    "Raney, K.",
                    "Devers, C.E.",
                    "Bundy, J."
                ],
                "citation": "Yonish, L., Raney, K., Devers, C.E., Bundy, J. (2023). No Room for Redemption: Toward an Understanding of Cancellation as an Organizational Phenomenon. Annual Meeting of the Academy of Management.",
                "elite_journal": "",
                "journal_name": "Annual Meeting of the Academy of Management",
                "paper_title": "No Room for Redemption: Toward an Understanding of Cancellation as an Organizational Phenomenon",
                "year": "2023"
            },
            {
                "authors": [
                    "Devers, C.E."
                ],
                "citation": "Devers, C.E. (2023) Keynote speaker at the Pamplin Graduate Student Orientation.",
                "elite_journal": "null",
                "journal_name": "Keynote speaker at the Pamplin Graduate Student Orientation",
                "paper_title": "",
                "year": "2023"
            }
        ],
        "name": "C.E. Devers",
        "publications": [
            {
                "authors": [
                    "Gamache, D.L.",
                    "Devers, C.E.",
                    "Klein, F.B,",
                    "Hannigan, T."
                ],
                "citation": "Gamache, D.L., Devers, C.E., Klein, F.B, & Hannigan, T. (2023) Shifting perspectives: How scrutiny shapes the relationship between CEO gender and acquisition activity, Strategic Management Journal 44: 3012-3041.",
                "elite_journal": "Strategic Management Journal",
                "journal_name": "Strategic Management Journal 44: 3012-3041",
                "paper_title": "Shifting perspectives: How scrutiny shapes the relationship between CEO gender and acquisition activity",
                "year": "2023"
            },
            {
                "authors": [
                    "Mah, J.",
                    "Kolev, K.",
                    "McNamara, G.",
                    "Devers, C.E."
                ],
                "citation": "Mah, J., Kolev, K., McNamara, G., Pan., L. & Devers, C.E. (2023) Women in the C-suite: A review and agenda of the challenges, opportunities, and impact of female top executives. In press. Academy of Management Annals 17: 586-625.",
                "elite_journal": "",
                "journal_name": "Academy of Management Annals 17: 586-625",
                "paper_title": "Women in the C-suite: A review and agenda of the challenges, opportunities, and impact of female top executives. In press",
                "year": "2023"
            },
            {
                "authors": [
                    "Gabriel, A.S.",
                    "Allen, T.D.",
                    "Devers, C.E.",
                    "Eby, L.T.",
                    "Gilson, L.L.",
                    "Hebl, M.",
                    "Kehoe, R.R.",
                    "King, E.B.",
                    "Ladge, J.J,",
                    "Little, L.M.",
                    "Schleicher, D.J.",
                    "Shockey, K.M.",
                    "Klotz, A.C.",
                    "Rosen, C.C."
                ],
                "citation": "Gabriel, A.S., Allen, T.D., Devers, C.E., Eby, L.T., Gilson, L.L., Hebl, M., Kehoe, R.R. King, E.B., Ladge, J.J, Little, L.M., Schleicher, D.J., Shockey, K.M., Klotz, A.C., & Rosen, C.C. (2023) A call to action: The imperative of supporting women scholars who have caregiving demands, Focal article: Industrial and Organizational Psychology, 16: 187-210.",
                "elite_journal": "",
                "journal_name": "Focal article: Industrial and Organizational Psychology",
                "paper_title": "A call to action: The imperative of supporting women scholars who have caregiving demands",
                "year": "2023"
            }
        ]
    },
    {
        "bookChapters": [],
        "conferences": [
            {
                "authors": [
                    "Gnyawali, D.R."
                ],
                "citation": "Gnyawali, D.R. “Managing Interdependence in Strategic Alliances”. Presented at a Symposium at the 2023 International Conference of the Strategic Management Society, Toronto, Canada.",
                "elite_journal": "",
                "journal_name": "Presented at a Symposium at the  International Conference of the Strategic Management Society",
                "paper_title": "Managing Interdependence in Strategic Alliances",
                "year": "2023"
            },
            {
                "authors": [
                    "Roehrich, J.",
                    "Squire, B.",
                    "Taubeneder, R.",
                    "Tyler, B.",
                    "Gnyawali, D.R."
                ],
                "citation": "Roehrich, J., Squire, B., Taubeneder, R., Tyler, B., & Gnyawali, D.R. 2023. “Managing Coopetition in a Multiparty Supplier Alliance”. 2023 Academy of Management Conference, Boston.",
                "elite_journal": "",
                "journal_name": "2023 Academy of Management Conference",
                "paper_title": "Managing Coopetition in a Multiparty Supplier Alliance",
                "year": "2023"
            }
        ],
        "name": "Devi Gnyawali",
        "publications": [
            {
                "authors": [
                    "Rai, R.",
                    "Gnyawali, D.R.",
                    "Bhatt, H."
                ],
                "citation": "Rai, R., Gnyawali, D.R., & Bhatt, H. 2023. Walking the Tightrope: Coopetition Capability Construct and its Role in Value Creation. Journal of Management, 49, 7: 2354-2386.",
                "elite_journal": "Journal of Management",
                "journal_name": "Journal of Management",
                "paper_title": "Walking the Tightrope: Coopetition Capability Construct and its Role in Value Creation",
                "year": "2023"
            }
        ]
    }
]

# Specify the output path for your Excel file
output_path = './output.xlsx'

# Convert JSON to Excel
json_to_excel(data, output_path)
