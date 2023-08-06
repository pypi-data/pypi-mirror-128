from BloomTechLib.Analysis.csv_similarity import csv_similarity_score


# Files
true_data = "data/csv_true.csv"
test_data = "data/csv_test.csv"

# Similarity
average_score = csv_similarity_score(
    true_data,
    test_data,
)

# Output
print("\n# Data Analysis Examples")
print("## CSV similarity score example")
print(f"\t• True Source: {true_data}")
print(f"\t• Test Source: {test_data}")
print(f"\t• Similarity Score: {100 * average_score:.2f}%")
print("...")
