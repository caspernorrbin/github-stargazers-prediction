import pandas as pd

def extract_line(filename, num_lines):
    df = pd.read_csv(filename)
    samples = df.sample(num_lines)
    samples.to_csv('sample_repos.csv', index=False)
    print(samples)



def main():
    extract_line('top_repos.csv', 7)


if __name__ == '__main__':
    main()
