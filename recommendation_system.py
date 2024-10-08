# -*- coding: utf-8 -*-
"""REcommendation_system.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nUUuNry0uC8fG1dHqpEVm30lTKfUNj3M
"""

import pandas as pd

df = pd.read_csv("symtoms_df.csv")

df.head(10)

sym1 = df['Symptom_1'].unique()
sym2 = df['Symptom_2'].unique()
sym3 = df['Symptom_3'].unique()

total_sym = set(sym1)
total_sym.update(sym2)
total_sym.update(sym3)

total_sym

len(total_sym)

all_symptoms = list(total_sym)

all_symptoms = [symptom.strip() for symptom in all_symptoms]

print(len(all_symptoms))

diseases = df['Disease'].unique()

len(diseases)

disease_symptoms_df = pd.DataFrame(index=diseases, columns=all_symptoms)
disease_symptoms_df = disease_symptoms_df.fillna(0)

disease_symptoms_df.head(10)

for index, row in df.iterrows():
       disease = row['Disease']
       symptoms = [row['Symptom_1'], row['Symptom_2'], row['Symptom_3']]
       for symptom in symptoms:
           if symptom in disease_symptoms_df.columns:
               disease_symptoms_df.loc[disease, symptom] = 1

disease_symptoms_df.head(10)

disease_symptoms_df.to_csv('disease_symptoms.csv', index=True)

biological_data = pd.read_csv("Training.csv")

biological_data.head(10)

bio_sym = list(biological_data.columns)

i = 1
for sym in bio_sym:
  if sym in all_symptoms:
    print(i, sym)
    i+= 1

not_neces = []
for sym in bio_sym:
  if sym not in all_symptoms and sym != 'prognosis':
    not_neces.append(sym)

not_neces

biological_data.drop(columns=not_neces, inplace=True)

subset_300 = biological_data.sample(n=300, random_state=42)

subset_300.columns

subset_final = subset_300.drop(['prognosis'], axis =1)
subset_final.to_csv('subset_final.csv', index=False)

#content based filtering

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

subset_final = pd.read_csv("subset_final.csv")
disease_symptoms_df = pd.read_csv("disease_symptoms.csv", index_col=0)

subset_final = subset_final.reindex(sorted(subset_final.columns), axis=1)
disease_symptoms_df = disease_symptoms_df.reindex(sorted(disease_symptoms_df.columns), axis=1)

similarity_matrix = cosine_similarity(subset_final, disease_symptoms_df)

def predict_disease(user_symptoms):
  similarity_scores = cosine_similarity([user_symptoms], disease_symptoms_df)
  most_similar_disease_index = similarity_scores.argmax()
  predicted_disease = disease_symptoms_df.index[most_similar_disease_index]
  return predicted_disease

predictions = []
for index, row in subset_final.iterrows():
  predicted_disease = predict_disease(row)
  predictions.append(predicted_disease)

subset_final['predicted_disease'] = predictions

#content based
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

subset_final = pd.read_csv("subset_final.csv")
disease_symptoms_df = pd.read_csv("disease_symptoms.csv", index_col=0)

subset_final = subset_final.reindex(sorted(subset_final.columns), axis=1)
disease_symptoms_df = disease_symptoms_df.reindex(sorted(disease_symptoms_df.columns), axis=1)

def predict_disease(user_symptoms):
  similarity_scores = cosine_similarity([user_symptoms], disease_symptoms_df)
  most_similar_disease_index = similarity_scores.argmax()
  predicted_disease = disease_symptoms_df.index[most_similar_disease_index]
  return predicted_disease

predictions = []
for index, row in subset_final.iterrows():
  predicted_disease = predict_disease(row)
  predictions.append(predicted_disease)

subset_final['predicted_disease_content'] = predictions

new_patients = pd.read_csv("subset_final.csv")
old_patients = pd.read_csv("Training.csv")
old_patients.drop(columns=not_neces, inplace=True)
old_patients.drop(columns=['prognosis'], inplace=True)
old_patients.head(5)

old_patients.index = range(1, len(old_patients) + 1)
old_patients.head(5)

new_patients = new_patients.reindex(sorted(old_patients.columns), axis=1)
old_patients = old_patients.reindex(sorted(old_patients.columns), axis=1)

def predict_patient(user_symptoms):
    similarity_scores = cosine_similarity([user_symptoms], old_patients.values)
    most_similar_patient_index = np.argmax(similarity_scores)
    predicted_patient = old_patients.index[most_similar_patient_index]
    return predicted_patient

predictions = []
for index, row in new_patients.iterrows():
    predicted_patient = predict_patient(row.values)  # Pass the row values as symptoms
    predictions.append(predicted_patient)

# Assign the predictions to the new column
new_patients['predicted_patient_id_collaborative'] = predictions









# prompt: what is worng in the above

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# ... (Your existing code) ...

# Issue: In collaborative filtering, you are trying to predict the patient ID based on patient's symptoms.
# However, predicting the patient ID directly based on symptoms is not a typical collaborative filtering task.
# Collaborative filtering usually aims to predict ratings/preferences (e.g., disease likelihood) based on the similarity of users/patients.

# Possible Solutions:
# 1. Predict disease based on patient similarity using collaborative filtering:

# - Create a user-item matrix where users are patients and items are diseases.
# - The matrix values can represent the likelihood of a patient having a certain disease.
# - Use cosine similarity to find similar patients and predict diseases based on what similar patients have.

# Example approach:

# Create a user-item matrix (replace with actual disease predictions)
# user_item_matrix = pd.DataFrame(index=old_patients.index, columns=diseases)
# user_item_matrix = user_item_matrix.fillna(0)

# # Fill the matrix based on predictions or actual disease data if available.
# # (This is crucial for accurate collaborative filtering)
# # For example, if patient 1 is predicted to have disease A with high probability, user_item_matrix.loc[1, 'Disease A'] = 1.

# def predict_disease_collaborative(user_symptoms):
#   similarity_scores = cosine_similarity([user_symptoms], old_patients)
#   most_similar_patient_index = similarity_scores.argmax()
#   similar_patient_id = old_patients.index[most_similar_patient_index]
#   predicted_disease = user_item_matrix.loc[similar_patient_id].idxmax()
#   return predicted_disease

# predictions_collaborative = []
# for index, row in old_patients.iterrows():
#   predicted_disease_collab = predict_disease_collaborative(row)
#   predictions_collaborative.append(predicted_disease_collab)

# subset_final['predicted_disease_collaborative'] = predictions_collaborative


# 2. Improve content-based filtering:
# - Ensure your disease_symptoms_df is accurately populated.
# - Consider using a more sophisticated similarity metric or algorithm.
# - Tune parameters if you are using a machine learning model for content-based prediction.


# ... (Rest of your code) ...

# It's important to note that collaborative filtering often requires a significant amount of user/patient data for accurate predictions.
# With a small dataset, the performance might not be as good.

# By addressing these issues, you can make the code more robust and effective for disease prediction using both content-based and (potentially) collaborative filtering.



