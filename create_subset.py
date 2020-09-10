import random

data = []
labels = []

with open("abstracts_pdf.tsv") as f:
	for line in f.readlines():
		data.append(line.split('\t'))

with open("abstracts_pdf_anns.csv") as f:
	for line in f.readlines():
		labels.append(line.split(','))

random.shuffle(data)

train_subset = data[:3000]

test_subset = data[3000:4000]

validation_subset = data[4000:5000]

train_labels = []
test_labels = []
validation_labels = []

train_set = set([line[0] for line in train_subset])
test_set = set([line[0] for line in test_subset])
validation_set = set([line[0] for line in validation_subset])

for label in labels:
	if label[0] in train_set:
		train_labels.append(label)
	if label[0] in test_set:
		test_labels.append(label)
	if label[0] in validation_set:
		validation_labels.append(label)


with open("train_data.csv", "w") as f:
	text = ""
	for line in train_subset:
		text += "\t".join(line)
	f.write(text)

with open("test_data.csv", "w") as f:
	text = ""
	for line in test_subset:
		text += "\t".join(line)
	f.write(text)

with open("validation_data.csv", "w") as f:
	text = ""
	for line in validation_subset:
		text += "\t".join(line)
	f.write(text)

with open("train_labels.csv", "w") as f:
	text = ""
	for line in train_labels:
		text += "\t".join(line)
	f.write(text)

with open("test_labels.csv", "w") as f:
	text = ""
	for line in test_labels:
		text += "\t".join(line)
	f.write(text)

with open("validation_labels.csv", "w") as f:
	text = ""
	for line in validation_labels:
		text += "\t".join(line)
	f.write(text)
