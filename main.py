import os
import json
from difflib import SequenceMatcher
from termcolor import cprint
from pyfiglet import figlet_format
import matplotlib.pyplot as plt
import time

def load_questions(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data["questions"]

def print_gerdinfo_logo():
    cprint(figlet_format('GERDINFO', font='starwars'), 'white', 'on_green', attrs=['bold'])

def typing_animation(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_gerdinfo_logo()

def display_question_count(total_questions, answered_questions):
    print(f"[Pertanyaan: {answered_questions}/{total_questions}]")

def introduction():
    clear_screen()
    typing_animation("Selamat datang di sistem pakar diagnosa penyakit GERD/Maag.")
    nama = input("Masukkan nama Anda: ")
    clear_screen()
    
    typing_animation(f"Halo {nama}, ingin bertanya sama sistem pakar sekarang? (Y/T): ")
    jawaban = input().upper()
    clear_screen()

    total_questions = 0
    answered_questions = 0

    while jawaban not in ('Y', 'T'):
        typing_animation("Hanya masukkan Y atau T.")
        jawaban = input(f"Halo {nama}, ingin bertanya sama sistem pakar sekarang? (Y/T): ").upper()
        clear_screen()

    if jawaban == 'Y':
        typing_animation(f"Halo {nama}, selamat datang! Kami akan memberikan list pertanyaan untuk mendeteksi gejala penyakit GERD/Maag.")
        input("Tekan Enter untuk melanjutkan...")
        clear_screen()

        # Count the total number of questions
        total_questions = len(load_questions('questions.json'))

    return nama, total_questions, answered_questions  # Return the entered name, total number of questions, and answered questions

def calculate_similarity(str1, str2):
    matcher = SequenceMatcher(None, str1, str2)
    return matcher.ratio()

def recommend_disease(answers, nama, total_questions, answered_questions):
    diseases = {
        "GERD": 0,
        "Maag": 0
    }

    with open('questions.json', 'r') as file:
        data = json.load(file)
        questions = data["questions"]

    for question_data in questions:
        os.system('cls' if os.name == 'nt' else 'clear')  # Membersihkan layar
        print_gerdinfo_logo()
        display_question_count(total_questions, answered_questions)
        question = question_data["question"]
        related_to = question_data.get("related_to", [])

        response = input(question + " (Y/T): ")
        answers.append(response.upper())
        answered_questions += 1

        similarity_score = calculate_similarity(answers[-1], 'Y')
        for disease in related_to:
            if similarity_score > 0.6:
                diseases[disease] += similarity_score * 10  # Scaling to 1-10

    recommended_disease = max(diseases, key=diseases.get)

    # Tampilkan hasil rekomendasi
    
    clear_screen()
    typing_animation(f"Berdasarkan hasil, pasien atas nama {nama} mungkin mengalami penyakit {recommended_disease} dengan skor rekomendasi {diseases[recommended_disease]:.2f}.")

    # Tampilkan diagram Bar Chart hasil rekomendasi
    labels = list(diseases.keys())
    values = list(diseases.values())

    plt.bar(labels, values, color=['blue', 'orange'])
    plt.title(f"Rekomendasi Penyakit untuk {nama}\n(mungkin mengalami {recommended_disease})")
    plt.xlabel('Penyakit')
    plt.ylabel('Skor Rekomendasi (1-10)')
    plt.show()

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    nama, total_questions, answered_questions = introduction()
    questions = load_questions('questions.json')
    answers = []

    for question_data in questions:
        os.system('cls' if os.name == 'nt' else 'clear')  # Membersihkan layar
        print_gerdinfo_logo()
        display_question_count(total_questions, answered_questions)
        question = question_data["question"]
        response = input(question + " (Y/T): ")
        answers.append(response.upper())
        answered_questions += 1
        if response.upper() == 'T':
            break  # Hentikan loop jika jawaban T

    recommend_disease(answers, nama, total_questions, answered_questions)

if __name__ == "__main__":
    main()
