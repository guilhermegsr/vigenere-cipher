import os
import pandas as pd
import matplotlib.pyplot as plt
from crypto.vigenere import VigenereCipher
from analyser.vigenere_analyser import VigenereAnalyser


RESULTS_DIR = "results"
TEXTS_DIR = "texts"


def ensure_dirs():
    """Ensure results and texts directories exist."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(TEXTS_DIR, exist_ok=True)


def ic_table(analyser):
    """Convert IC scores into a DataFrame."""
    df = pd.DataFrame(
        analyser.key_length_scores.items(),
        columns=["Key Length", "Average IC"]
    ).sort_values("Key Length")
    return df


def plot_ic(analyser, filename):
    """Plot Index of Coincidence scores."""
    df = ic_table(analyser)
    plt.figure(figsize=(8, 5))
    plt.plot(df["Key Length"], df["Average IC"], marker="o")
    plt.xlabel("Key Length")
    plt.ylabel("Average IC")
    plt.title("Index of Coincidence vs Key Length")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig(os.path.join(RESULTS_DIR, filename), dpi=150)
    plt.close()


def column_table(analyser):
    """Convert column metrics into a DataFrame."""
    rows = []
    for col in analyser.column_metrics:
        rows.append({
            "Column Position": col["position"],
            "Best Shift": col["best_shift"],
            "Best Score": col["best_score"]
        })
    return pd.DataFrame(rows)


def plot_column_scores(analyser, col_index, filename):
    """Plot chi-squared scores for a given column."""
    col = analyser.column_metrics[col_index]
    shifts = list(col["scores"].keys())
    scores = list(col["scores"].values())

    plt.figure(figsize=(8, 5))
    plt.bar(shifts, scores)
    plt.xlabel("Shift (0 = A, 1 = B, ...)")
    plt.ylabel("Chi-squared Score")
    plt.title(f"Chi-squared Scores for Column {col_index}")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.savefig(os.path.join(RESULTS_DIR, filename), dpi=150)
    plt.close()


def choose_text_file():
    """List available .txt files and let user choose one."""
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

    # 5. Attack with analyser
    analyser = VigenereAnalyser(ciphertext, language=lang)
    recovered_key = analyser.analyse(max_len=15)

    print(f"Recovered key: {recovered_key}\n")

    # 6. Save metrics & plots
    df_ic = ic_table(analyser)
    df_ic.to_csv(os.path.join(RESULTS_DIR, "ic_scores.csv"), index=False)
    plot_ic(analyser, "ic_scores.png")

    df_col = column_table(analyser)
    df_col.to_csv(os.path.join(RESULTS_DIR, "column_metrics.csv"), index=False)

    for i in range(len(analyser.column_metrics)):
        plot_column_scores(analyser, i, f"column_{i}_scores.png")

    print(f"Results saved in '{RESULTS_DIR}/' folder.")


if __name__ == "__main__":
    main()
