from pathlib import Path
import sys

def wav2cat(filename):
    minute = filename.split('/')[0]
    cat = Path(filename).stem.split('_')[1]
    return minute, cat

def parse_index(index):
    data = Path(index).read_text().splitlines()
    mos_start = 17
    print(data[mos_start])
    min_out = []
    mos_out = []
    for i in range(50):
    	#parse audio name
        filename = data[mos_start + i * 2][12:-27]
        #parse wav 2 its minute and category
        minute, cat = wav2cat(filename)
        min_out.append(minute)
        mos_out.append(cat)
    return min_out, mos_out

def run(response_file, index_file):
	response = pd.read_csv(response_file, header=None).drop(0, axis=0).drop(0, axis=1)
	min_out, mos_out = parse_index(index_file)
	MOS = {"MOS_25min" :defaultdict(list), "MOS_15min":defaultdict(list)}
	for i in range(len(response)):
	    res = response.iloc[i]
	    for col in range(50):
	        score = int(res[col+1])
	        cat = mos_out[col]
	        minute = min_out[col]
	        MOS[minute][cat].append(score)
	return MOS



def summary(ans_dict):
	ans = {"MOS_25min" :dict(), "MOS_15min":dict()}
	for minute, v in MOS.items() :
	    for cat, answers in v.items():
	        ans[minute][cat] = sum(answers) / len(answers)
	print(ans)


if __name__ == '__main__':
	ans_dict = run(sys.argv[1], sys.argv[2])
	summary(ans_dict)