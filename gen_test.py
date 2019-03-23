from pathlib import Path
import pandas as pd
import random

def get_reference_txt():
    data = pd.read_csv('meta_f05.txt', sep='|', header=None)
    data[0] = [file.split('-')[2] for file in data[0]]
    data[2] = [line.replace(' ', '') for line in data[2]]
    id2text = {}
    for i in range(len(data)):
        id2text[data[0][i]] = data[2][i]
    return id2text



bold_line = "- - -"
nl = ["\n"] #new line
part1_explain = Path("template1.md").read_text().splitlines() + nl + [bold_line+'\n']
#part2_explain = Path("template2.md").read_text().splitlines() + nl + bold_line
#separate_line = nl*2 + bold_line  + nl*2
#define formats
no_format = "#### *No. {}-{}*"
AB_format = "#### {} audio : {}"
txt_format = "#### {}"
audio_format = "<audio src=\"{}\" controls preload></audio>"

if __name__ == "__main__" :
    id2text = get_reference_txt()
    for survey in Path('.').glob("CL*"):
        print("Preprocessing {}".format(survey))
        part1_out = []
        name_list = [audio for audio in Path(survey).rglob('MOS*/share/*.wav')]
        random.shuffle(name_list)
        for pid, name in enumerate(name_list):
            parent = '/'.join(name.parts[:-2])
            num = str(name.name).split('_')[0]
            idx = num.split('-')[2]
            txt = id2text [idx]
            mos_audio = [audio for audio in Path(parent).rglob(num+'*')]
            random.shuffle(mos_audio)
            part1_out.append(txt_format.format(txt))
            for i, file in enumerate(mos_audio):
                part1_out.append(no_format.format(pid+1, i+1))
                name = '/'.join(Path(file).parts[2:])
                part1_out.append(audio_format.format(name))   
            part1_out.append(bold_line)
        # part2_out = []
        # ab_dir = [dir_ for dir_ in Path(survey, 'AB-test').rglob('*min/*')]
        # random.shuffle(ab_dir)
        # for i, dir_ in enumerate(ab_dir) :
        #     audios = [file for file in dir_.glob('*.wav')]
        #     assert len(audios) == 2
        #     random.shuffle(audios)
        #     part2_out.append(no_format.format(i+1))
        #     for file, aorb in zip(audios, ["A", "B"]):
        #         name = '/'.join(Path(file).parts[1:])
        #         idx = name.split('/')[2]
        #         string = id2text[idx]
        #         part2_out.append(AB_format.format(aorb, string))
        #         part2_out.append(audio_format.format(name))

        # out = part1_explain + part1_out + separate_line + part2_explain + part2_out
        out = part1_explain + part1_out
        with open(Path(survey, "index.md"), 'w') as f:
            for line in out :
                f.write(line+'\n')
