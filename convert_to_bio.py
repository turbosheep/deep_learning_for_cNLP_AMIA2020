import spacy
from spacy.gold import biluo_tags_from_offsets

data = {}
labels = {}

with open("test_train_split/validation_data.tsv") as f:
	for line in f.readlines():
		split = line.strip().split("\t")
		data[split[0]] = split[1]

with open("test_train_split/validation_labels.tsv") as f:
	for line in f.readlines()[1:]:
		split = line.strip().split("\t")
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

ids = list(data.keys())

bio_tags = []
sentences = []

for id in ids:
	doc = nlp(data[id])
	offsets = []
	if id in labels.keys():
		offsets = labels[id]

	labs = biluo_tags_from_offsets(doc,offsets)

	for sent in doc.sents:
		s = []
		l = []
		contains_positive = False
		for word in sent:
			s.append(word.lower_)
			label = labs[word.i]
			if label == '-':
				l.append("O")
			else:
				l.append(labs[word.i])
			if labs[word.i] != 'O' and labs[word.i] != '-':
				contains_positive = True
		if len(s) > 150:
			continue
		if contains_positive:
			bio_tags.append(id+"\t"+" ".join(l))
			sentences.append(id+"\t"+" ".join(s))


with open("test_train_split/validation_labels_bio.tsv", "w") as f:
	f.write("\n".join(bio_tags))

with open("test_train_split/validation_data_pretokenized.tsv","w") as f:
	f.write("\n".join(sentences))

