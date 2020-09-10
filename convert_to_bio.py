import spacy
from spacy.gold import biluo_tags_from_offsets

data = {}
labels = {}

with open("test_train_split/train_data.csv") as f:
	for line in f.readlines():
		split = line.split("\t")
		data[split[0]] = split[1]

with open("test_train_split/train_labels.csv") as f:
	for line in f.readlines()[1:]:
		split = line.split("\t")
		if split[0] in labels.keys():
			overlap = False
			for label in labels[split[0]]:
				lstart = label[0]
				lend = label[1]
				start = int(split[1])
				end = int(split[2])
				if lstart < end and start < lend:
					overlap = True
			if not overlap:
				labels[split[0]].append((int(split[1]),int(split[2]),split[3]))
		else:
			labels[split[0]] = [(int(split[1]),int(split[2]),split[3])]


nlp = spacy.load("en_core_web_sm")

ids = labels.keys()

bios = []
tokens = []

for id in ids:
	doc = nlp(data[id])
	bios.append(id+"\t"+" ".join(biluo_tags_from_offsets(doc,labels[id])))
	tokens.append(id+"\t"+" ".join([token.lower_ for token in doc]))
		

with open("train_labels_bio.tsv", "w") as f:
	f.write("\n".join(bios))

with open("train_data_pretokenized.tsv","w") as f:
	f.write("".join(tokens))

