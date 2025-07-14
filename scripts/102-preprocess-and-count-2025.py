import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer

def load_data(start_year=2010, end_year=2024):
    print("Loading data...", flush=True)

    df = pd.read_parquet(
        INPUT_FOLDER + "pubmed_baseline_2025.parquet.gzip",
        engine="pyarrow",
    )

    if end_year == 2025:
        df2 = pd.read_parquet(
            INPUT_FOLDER + "pubmed_daily_updates_2025_v1.parquet.gzip",
            engine="pyarrow",
        )

        df = pd.concat((df, df2))
        df = df.groupby(["PMID"]).last()

    print(f"Found {len(df)} papers.", flush=True)

    df = df[(df.Year >= start_year) & (df.Year <= end_year)]
    print(
        f"Kept {len(df)} papers from {start_year}--{end_year}.", flush=True
    )  # 15103887

    return df


# RESULTS_FOLDER = '../results/'
RESULTS_FOLDER = ""

INPUT_FOLDER = "/gpfs01/berens/data/data/pubmed_processed/"

# df = load_data(start_year=2010, end_year=2025) # 15892778 papers

# cleanup_abstracts_inplace(df) # Note: I did not run this here

# vectorizer = CountVectorizer(binary=True, min_df=1e-6)
# X = vectorizer.fit_transform(df.AbstractText.values)  # ~30 min
# words = vectorizer.get_feature_names_out()
#   
# print(f"Count matrix computed: {X.shape}", flush=True)  # 15892778 x 374172
#
# pickle.dump(X, open(RESULTS_FOLDER + "counts-2025jul.pkl", "wb"))
# pickle.dump([words, df.Year.values, df.Month.values], open(RESULTS_FOLDER + "words-2025jul.pkl", "wb"))

X = pickle.load(open(RESULTS_FOLDER + "counts-2025jul.pkl", "rb"))
words, Year, Month = pickle.load(open(RESULTS_FOLDER + "words-2025jul.pkl", "rb"))

years = np.arange(2010, 2026)
counts = np.zeros((words.size, years.size, 12))
totals = np.zeros((years.size, 12))

for i, year in enumerate(years):
    for month in range(12):
        ind = (Year == year) & (Month == month + 1)
        counts[:, i, month] = np.array(np.sum(X[ind, :], axis=0)).ravel()
        totals[i, month] = np.sum(ind)

chatgptwords_rare = [
    "accentuates", "acknowledges", "acknowledging", "addresses", "adept", "adhered", "adhering", "advancement", "advancements", "advancing", "advocates", "advocating", "affirming", "afflicted", "aiding", "akin", "align", "aligning", "aligns", "alongside", "amidst", "assessments", "attains", "attributed", "augmenting", "avenue", "avenues", "bolster", "bolstered", "bolstering", "broader", "burgeoning", "capabilities", "capitalizing", "categorized", "categorizes", "categorizing", "combating", "commendable", "compelling", "complicates", "complicating", "comprehending", "comprising", "consequently", "consolidates", "contributing", "conversely", "correlating", "crafted", "crafting", "culminating", "customizing", "delineates", "delve", "delved", "delves", "delving", "demonstrating", "dependability", "dependable", "detailing", "detrimentally", "diminishes", "diminishing", "discern", "discerned", "discernible", "discerning", "displaying", "disrupts", "distinctions", "distinctive", "elevate", "elevates", "elevating", "elucidate", "elucidates", "elucidating", "embracing", "emerges", "emphasises", "emphasising", "emphasize", "emphasizes", "emphasizing", "employing", "employs", "empowers", "emulating", "emulation", "enabling", "encapsulates", "encompass", "encompassed", "encompasses", "encompassing", "endeavors", "endeavours", "enduring", "enhancements", "enhances", "ensuring", "equipping", "escalating", "evaluates", "evolving", "exacerbating", "examines", "exceeding", "excels", "exceptional", "exceptionally", "exerting", "exhibiting", "exhibits", "expedite", "expediting", "exploration", "explores", "facilitated", "facilitates", "facilitating", "featuring", "formidable", "fostering", "fosters", "foundational", "furnish", "garnered", "garnering", "gauged", "grappling", "groundbreaking", "groundwork", "harness", "harnesses", "harnessing", "heighten", "heightened", "hinder", "hinges", "hinting", "hold", "holds", "illuminates", "illuminating", "imbalances", "impacting", "impede", "impeding", "imperative", "impressive", "inadequately", "incorporates", "incorporating", "influencing", "inherent", "initially", "innovative", "inquiries", "integrates", "integrating", "integration", "interconnectedness", "interplay", "intricacies", "intricate", "intricately", "introduces", "invaluable", "investigates", "involves", "juxtaposed", "leverages", "leveraging", "maintaining", "merges", "methodologies", "meticulous", "meticulously", "multifaceted", "necessitate", "necessitates", "necessitating", "necessity", "notable", "noteworthy", "nuanced", "nuances", "offering", "optimizing", "orchestrating", "outlines", "overlook", "overlooking", "paving", "persist", "pinpoint", "pinpointed", "pinpointing", "pioneering", "pioneers", "pivotal", "poised", "pose", "posed", "poses", "posing", "predominantly", "preserving", "pressing", "promise", "pronounced", "propelling", "realm", "realms", "recognizing", "refine", "refines", "refining", "remarkable", "renowned", "revealing", "reveals", "revolutionize", "revolutionizing", "revolves", "scrutinize", "scrutinized", "scrutinizing", "seamless", "seamlessly", "seeks", "serves", "serving", "shaping", "shedding", "showcased", "showcases", "showcasing", "signifying", "solidify", "spanned", "spanning", "spurred", "stands", "stemming", "strategically", "streamline", "streamlined", "streamlines", "streamlining", "struggle", "substantiated", "substantiates", "surged", "surmount", "surpass", "surpassed", "surpasses", "surpassing", "swift", "swiftly", "thorough", "transformative", "typically", "ultimately", "uncharted", "uncovering", "underexplored", "underscore", "underscored", "underscores", "underscoring", "unexplored", "unlocking", "unparalleled", "unraveling", "unveil", "unveiled", "unveiling", "unveils", "uphold", "upholding", "urging", "utilizes", "varying", "versatility", "warranting", "yielding"
]

chatgptwords_common = [
    "exhibited",
    "crucial",
    "additionally",
    "within",
    "notably",
    "insights",
    "comprehensive",
    "across",
    "particularly",
    "enhancing",
]
    
ind_words_common = np.isin(words, chatgptwords_common)
ind_words_rare = np.isin(words, chatgptwords_rare)

group_counts = np.zeros((3, years.size, 12), dtype=int)
for i, year in enumerate(years):
    for month in range(12):
        ind = (Year == year) & (Month == month + 1)
        for j, ind_words in enumerate([ind_words_common, ind_words_rare]):
            group_counts[j, i, month] = np.sum(np.sum(X[ind, :][:, ind_words], axis=1) > 0)
            group_counts[2, i, month] = np.sum(ind)

np.concatenate(
    (
        counts[np.isin(words, ["delves", "potential"])] / totals,
        group_counts[:2] / group_counts[2]
    )
)
