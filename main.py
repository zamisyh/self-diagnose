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

def introduction():
    clear_screen()
    typing_animation("Selamat datang di sistem pakar diagnosa penyakit GERD/Maag.")
    nama = input("Masukkan nama Anda: ")
    
    clear_screen()
    
    typing_animation(f"Halo {nama}, ingin bertanya sama sistem pakar sekarang? (Y/T): "); jawaban = input().upper()
    
    clear_screen()


    while jawaban not in ('Y', 'T'):
        typing_animation("Hanya masukkan Y atau T.")
        jawaban = input("Halo {nama}, ingin bertanya sama sistem pakar sekarang? (Y/T): ").upper()
        clear_screen()


    if jawaban == 'Y':
        typing_animation(f"Halo {nama}, selamat datang! kami akan memberikan list pertanyaan untuk mendeteksi gejala penyakit gerd/maag.")
    return nama  # Return the entered name

def calculate_similarity(str1, str2):
    matcher = SequenceMatcher(None, str1, str2)
    return matcher.ratio()

def recommend_disease(answers, nama):
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
        question = question_data["question"]
        related_to = question_data.get("related_to", [])

        response = input(question + " (Y/T): ")
        answers.append(response.upper())

        similarity_score = calculate_similarity(answers[-1], 'Y')
        for disease in related_to:
            if similarity_score > 0.6:
                diseases[disease] += similarity_score * 10  # Scaling to 1-10

    recommended_disease = max(diseases, key=diseases.get)

    # Tampilkan diagram Bar Chart hasil rekomendasi
    labels = list(diseases.keys())
    values = list(diseases.values())

    plt.bar(labels, values, color=['blue', 'orange'])
    plt.title(f"Rekomendasi Penyakit untuk {nama}\n(mungkin mengalami {recommended_disease})")
    plt.xlabel('Penyakit')
    plt.ylabel('Skor Rekomendasi (1-10)')
    plt.show()

    # Tampilkan hasil rekomendasi
    typing_animation(f"Berdasarkan hasil, pasien atas nama {nama} mungkin mengalami penyakit {recommended_disease} dengan skor rekomendasi {diseases[recommended_disease]:.2f}.")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    nama = introduction()
    questions = load_questions('questions.json')
    answers = []

    for question_data in questions:
        os.system('cls' if os.name == 'nt' else 'clear')  # Membersihkan layar
        print_gerdinfo_logo()
        question = question_data["question"]
        response = input(question + " (Y/T): ")
        answers.append(response.upper())
        if response.upper() == 'T':
            break  # Hentikan loop jika jawaban T

    recommend_disease(answers, nama)

if __name__ == "__main__":
    main()
