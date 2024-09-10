"""
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords_tfidf(cleaned_text, num_keywords=10):
    # Initialize the TF-IDF Vectorizer with adjusted parameters
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.85, min_df=1, max_features=1000)

    # Fit and transform the text data
    tfidf_matrix = vectorizer.fit_transform([cleaned_text])

    # Get the feature names (words)
    feature_names = vectorizer.get_feature_names_out()

    # Extract the top keywords and their scores
    tfidf_scores = tfidf_matrix.toarray()[0]
    keyword_indices = tfidf_scores.argsort()[-num_keywords:][::-1]
    keywords = [(feature_names[i], tfidf_scores[i]) for i in keyword_indices]

    return keywords

# Example usage
cleaned_text = 
film title the secret agent film release date 01012023 film duration 120 minutes payment terms 100000 upfront 50000 upon completion rights granted worldwide distribution rights territory global production budget 1000000 revenue sharing 50 producer 50 actor agency marketing and promotion shared responsibility insurance producer to provide insurance coverage filming locations los angeles new york london screenplay rights owned by xyz productions signatures party a party b additional terms 1 the producer shall have final creative control over the film 2 the actor agency shall provide casting services for the film 3 both parties agree to abide by the terms and conditions outlined in this contract human rights considerations 1 the producer and actor agency commit to upholding the highest standards of human rights throughout the production process 2 all cast and crew members shall be treated with dignity and respect free from discrimination harassment and exploitation 3 the producer shall ensure safe working conditions and fair labor practices in accordance with local and international labor laws legal compliance and ethical standards 1 both parties agree to comply with all applicable laws and regulations including labor laws health and safety standards and antidiscrimination laws 2 the producer shall obtain all necessary permits and licenses required for filming in designated locations 3 any violations of laws or ethical standards may result in immediate termination of this contract key business considerations this contract includes critical business elements such as 1 clearly defined roles and responsibilities of each party 2 detailed financial terms including budget payment structure and revenue sharing 3 scope of rights granted and territories covered negotiating film industry contracts human rights perspective 1 understand the importance of ethical practices and human rights in negotiations 2 ensure that all terms reflect a commitment to fair treatment and respect for individuals involved in the production 3 seek legal advice to protect human rights and ensure compliance with relevant laws common pitfalls in film industry contracts human rights risks 1 failing to address human rights issues can lead to reputational damage and legal consequences 2 lack of clarity in labor practices may result in exploitation or unsafe working conditions 3 ignoring local laws and regulations can expose both parties to legal liabilities drafting effective film industry contracts best practices 1 use clear and unambiguous language to avoid misunderstandings regarding human rights obligations 2 include all relevant business terms and conditions to create a comprehensive agreement 3 regularly review and update contracts to adapt to changes in laws and ethical standards enforcing film industry contracts legal remedies and human rights 1 understand the consequences and remedies for breach of contract particularly regarding human rights violations 2 be prepared to take legal action if necessary to protect human rights and enforce contract terms 3 consider alternative dispute resolution methods such as mediation or arbitration to resolve conflicts efficiently recent developments in film industry contract law human rights implications 1 increasing emphasis on ethical production practices and human rights in industry standards 2 changes in regulations regarding labor rights and protections for cast and crew members 3 growing awareness of the impact of film production on local communities and the environment

keywords = extract_keywords_tfidf(cleaned_text)
print("Extracted Keywords (TF-IDF):", keywords)
"""
# M2: RAKE (Rapid Automatic Keyword Extraction) Method

from rake_nltk import Rake

def extract_keywords_rake(text, num_keywords=10):
    # Initialize RAKE with stopwords from nltk
    r = Rake()

    # Extract keywords/phrases from text
    r.extract_keywords_from_text(text)

    # Get the ranked phrases with their scores
    ranked_phrases = r.get_ranked_phrases_with_scores()

    # Return the top 'num_keywords' phrases
    return ranked_phrases[:num_keywords]

# Example usage
cleaned_text = """
film title the secret agent film release date 01012023 film duration 120 minutes payment terms 100000 upfront 50000 upon completion rights granted worldwide distribution rights territory global production budget 1000000 revenue sharing 50 producer 50 actor agency marketing and promotion shared responsibility insurance producer to provide insurance coverage filming locations los angeles new york london screenplay rights owned by xyz productions signatures party a party b additional terms 1 the producer shall have final creative control over the film 2 the actor agency shall provide casting services for the film 3 both parties agree to abide by the terms and conditions outlined in this contract human rights considerations 1 the producer and actor agency commit to upholding the highest standards of human rights throughout the production process 2 all cast and crew members shall be treated with dignity and respect free from discrimination harassment and exploitation 3 the producer shall ensure safe working conditions and fair labor practices in accordance with local and international labor laws legal compliance and ethical standards 1 both parties agree to comply with all applicable laws and regulations including labor laws health and safety standards and antidiscrimination laws 2 the producer shall obtain all necessary permits and licenses required for filming in designated locations 3 any violations of laws or ethical standards may result in immediate termination of this contract key business considerations this contract includes critical business elements such as 1 clearly defined roles and responsibilities of each party 2 detailed financial terms including budget payment structure and revenue sharing 3 scope of rights granted and territories covered negotiating film industry contracts human rights perspective 1 understand the importance of ethical practices and human rights in negotiations 2 ensure that all terms reflect a commitment to fair treatment and respect for individuals involved in the production 3 seek legal advice to protect human rights and ensure compliance with relevant laws common pitfalls in film industry contracts human rights risks 1 failing to address human rights issues can lead to reputational damage and legal consequences 2 lack of clarity in labor practices may result in exploitation or unsafe working conditions 3 ignoring local laws and regulations can expose both parties to legal liabilities drafting effective film industry contracts best practices 1 use clear and unambiguous language to avoid misunderstandings regarding human rights obligations 2 include all relevant business terms and conditions to create a comprehensive agreement 3 regularly review and update contracts to adapt to changes in laws and ethical standards enforcing film industry contracts legal remedies and human rights 1 understand the consequences and remedies for breach of contract particularly regarding human rights violations 2 be prepared to take legal action if necessary to protect human rights and enforce contract terms 3 consider alternative dispute resolution methods such as mediation or arbitration to resolve conflicts efficiently recent developments in film industry contract law human rights implications 1 increasing emphasis on ethical production practices and human rights in industry standards 2 changes in regulations regarding labor rights and protections for cast and crew members 3 growing awareness of the impact of film production on local communities and the environment
"""

keywords_rake = extract_keywords_rake(cleaned_text)
print("Extracted Keywords (RAKE):", keywords_rake)
