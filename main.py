import os
import pandas as pd
import matplotlib.pyplot as plt
from crypto.vigenere import VigenereCipher
from analyser.vigenere_analyser import VigenereAnalyser

# Directories for storing texts and results
RESULTS_DIR = "results"
TEXTS_DIR = "texts"


def ensure_dirs():
    """
    Ensure that the necessary directories exist.
    Creates 'results' and 'texts' folders if they do not exist.
    """
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(TEXTS_DIR, exist_ok=True)


def ic_table(analyser):
    """
    Convert the Index of Coincidence (IC) scores into a pandas DataFrame.
    
    Args:
        analyser (VigenereAnalyser): The analyser object containing IC scores.
    
    Returns:
        pd.DataFrame: DataFrame containing key lengths and their average IC.
    """
    df = pd.DataFrame(
        analyser.key_length_scores.items(),
        columns=["Key Length", "Average IC"]
    ).sort_values("Key Length")
    return df


def plot_ic(analyser, filepath):
    """
    Plot the Index of Coincidence (IC) scores and save as an image.
    
    Args:
        analyser (VigenereAnalyser): The analyser object containing IC scores.
        filepath (str): Path to save the plot image.
    """
    df = ic_table(analyser)
    plt.figure(figsize=(8, 5))
    plt.plot(df["Key Length"], df["Average IC"], marker="o")
    plt.xlabel("Key Length")
    plt.ylabel("Average IC")
    plt.title("Index of Coincidence vs Key Length")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig(filepath, dpi=150)
    plt.close()


def column_table(analyser):
    """
    Convert column-based analysis metrics into a pandas DataFrame.
    
    Args:
        analyser (VigenereAnalyser): The analyser object with column metrics.
    
    Returns:
        pd.DataFrame: DataFrame with best shift and score per column.
    """
    rows = []
    for col in analyser.column_metrics:
        rows.append({
            "Column Position": col["position"],
            "Best Shift": col["best_shift"],
            "Best Score": col["best_score"]
        })
    return pd.DataFrame(rows)


def plot_column_scores(analyser, col_index, filepath):
    """
    Plot chi-squared scores for a specific column and save as an image.
    
    Args:
        analyser (VigenereAnalyser): The analyser object containing scores.
        col_index (int): Index of the column to plot.
        filepath (str): Path to save the plot image.
    """
    col = analyser.column_metrics[col_index]
    shifts = list(col["scores"].keys())
    scores = list(col["scores"].values())

    plt.figure(figsize=(8, 5))
    plt.bar(shifts, scores)
    plt.xlabel("Shift (0 = A, 1 = B, ...)")
    plt.ylabel("Chi-squared Score")
    plt.title(f"Chi-squared Scores for Column {col_index}")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.savefig(filepath, dpi=150)
    plt.close()


def choose_text_file():
    """
    List available .txt files in the TEXTS_DIR and allow the user to choose one.
    
    Returns:
        str or None: Full path to the selected text file, or None if selection is invalid.
    """
    files = [f for f in os.listdir(TEXTS_DIR) if f.endswith(".txt")]
    if not files:
        print(f"No .txt files found in '{TEXTS_DIR}'.")
        return None

    print("\nAvailable text files:")
    for i, f in enumerate(files):
        print(f"[{i}] {f}")

    choice = input("Choose a file by index: ")
    try:
        idx = int(choice)
        return os.path.join(TEXTS_DIR, files[idx])
    except (ValueError, IndexError):
        print("Invalid choice.")
        return None


def main():
    """
    Main program workflow:
    1. Ensure necessary directories exist.
    2. Get user inputs for encryption key and language.
    3. Let user choose a text file.
    4. Encrypt and decrypt the text using Vigenère cipher.
    5. Analyse the ciphertext to attempt key recovery.
    6. Save metrics and plots in a text-specific subfolder.
    """
    ensure_dirs()

    # 1. Ask user for encryption key
    key = input("Enter the key for encryption: ").strip().upper()

    # 2. Ask user for text language
    lang = input("Enter text language [pt/en]: ").strip().lower()
    if lang not in ["pt", "en"]:
        print("Invalid choice, defaulting to 'pt'")
        lang = "pt"

    # 3. Let user choose a text file
    text_path = choose_text_file()
    if not text_path:
        return

    # Create a folder specific to this text inside RESULTS_DIR
    text_name = os.path.splitext(os.path.basename(text_path))[0]
    result_path = os.path.join(RESULTS_DIR, text_name)
    os.makedirs(result_path, exist_ok=True)

    # Read plaintext from the chosen text file
    with open(text_path, "r", encoding="utf-8") as f:
        plaintext = f.read().strip()

    print("\nPlaintext (first 200 chars):")
    print(plaintext[:200], "...\n")

    # 4. Encrypt & Decrypt
    cipher = VigenereCipher(key)
    ciphertext = cipher.encrypt(plaintext)
    decrypted = cipher.decrypt(ciphertext)

    print(f"Key used for encryption: {key}")
    print(f"Ciphertext (first 200 chars): {ciphertext[:200]} ...\n")
    print(f"Decrypted (first 200 chars): {decrypted[:200]} ...\n")

    # 5. Analyse the ciphertext to recover key
    analyser = VigenereAnalyser(ciphertext, language=lang)
    recovered_key = analyser.analyse(max_len=15)

    print(f"Recovered key: {recovered_key}\n")

    # 6. Save metrics & plots in text-specific folder
    df_ic = ic_table(analyser)
    df_ic.to_csv(os.path.join(result_path, "ic_scores.csv"), index=False)
    plot_ic(analyser, os.path.join(result_path, "ic_scores.png"))

    df_col = column_table(analyser)
    df_col.to_csv(os.path.join(result_path, "column_metrics.csv"), index=False)

    for i in range(len(analyser.column_metrics)):
        plot_column_scores(analyser, i, os.path.join(result_path, f"column_{i}_scores.png"))

    print(f"Results saved in '{result_path}/' folder.")


if __name__ == "__main__":
    main()
