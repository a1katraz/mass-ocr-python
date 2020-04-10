import pandas

if __name__ == '__main__':
	df = pandas.read_csv('ACNo238_CombinedFile.csv', header=0, sep=',', encoding='utf-8')
	hist= df.groupby('Part No.')[' \t\t\tVoter ID'].nunique()
	hist.to_csv('booth_hist.csv', index=True)

