import glob

#the path to where the tree svgs are stored
treePath = 'trees/'

#the sheet dimensions in mm
sheetx = 390
sheety = 200

#the tree dimensions in mm
treex = 80
treey = 84

#the number of trees that will fit in a row
rowlen = 2 * sheetx//(treex + 10) - 1
print(rowlen)

#the number of trees that will fit in a column
collen = sheety//(treey + 10)
print(collen)

#the maximum number of trees that will fit on a sheet
treemax = rowlen * collen
print(treemax)

#a list contaning the paths of all the trees
trees = []
for tree in glob.glob(treePath + '*'):
	trees.append(tree)

row = []
sheet = []
sheets = []
for tree in trees:
	if len(row) == rowlen:
		sheet.append(row)
		row = []
		if len(sheet) == collen:
			sheets.append(sheet)
			sheet = []
	row.append(tree)

#the number of sheets required
sheetno = len(sheets)