import pandas as pd
import sys
import traceback
from collections import defaultdict

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 sql2py.py <inspections.csv> <chunk_size>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        chunk_size = int(sys.argv[2])
    except ValueError:
        print("Error: Chunk size must be an integer.")
        sys.exit(1)

    # Initialize data structures
    score_sums = defaultdict(float)
    count_dict = defaultdict(int)

    try:
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            # TODO: Filter chunk
            condition = (chunk["facility_name"].str.contains("COFFEE", case=False) & chunk["program_status"].str.contains("ACTIVE", case=False))
            df = chunk.loc[condition]

            # TODO: Group and aggregate
            if not df.empty:
                group = df.groupby("facility_name").agg(
                    avg_score = ('score', 'sum'),
                    records_count = ('score', 'count')
                ).reset_index()
                # TODO: Update aggregates
                if not group.empty:
                    for i in range(len(group)):
                        facility_name = str(group.iloc[i, 0])
                        score_sums[facility_name] += float(group.iloc[i, 1])
                        count_dict[facility_name] += int(group.iloc[i, 2])
            pass

    except Exception:
        traceback.print_exc()
        sys.exit(1)

    # print(f'score_sums: {len(score_sums)}')
    # print(f'count_dict: {len(count_dict)}')

    # TODO: Compute average scores
    # avg_score_dict = defaultdict(float)
    # if len(score_sums) == len(count_dict):
    #     for store in score_sums.keys():
    #         avg_score_dict[store] = round(score_sums[store]/count_dict[store], 6)
    # print(avg_score_dict)

    results = []
    for facility in sorted(score_sums):
        count = count_dict[facility]
        if count >= 10:
            avg_score = score_sums[facility] / count
            results.append((facility, avg_score))

    # TODO: Output results
    results.sort(key=lambda x: x[0])
    for facility, avg in results:
        print(f"{facility},{avg:.6f}")

    pd.DataFrame({
        'facility_name': [i[0]for i in results],
        'avg(score)': [f'{i[1]:.6f}' for i in results]}
    ).to_csv('./Tien-Ching_Hsieh_output.csv', index=True)

if __name__ == "__main__":
    main()
