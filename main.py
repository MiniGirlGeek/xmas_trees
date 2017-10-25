import glob

#the path to where the tree svgs are stored
treePath = 'trees/'

mmToPx = 2.83464102564

#the sheet dimensions in mm
sheetx = 600
sheety = 300

#the tree dimensions in mm
treex = 80
treey = 84

#the number of trees that will fit in a row
rowlen = 2 * sheetx//(treex + 25) - 1

#the number of trees that will fit in a column
collen = sheety//(treey + 10)

#the maximum number of trees that will fit on a sheet
treemax = rowlen * collen

#a list contaning the paths of all the trees
trees = []
for tree in glob.glob(treePath + '*'):
	trees.append(tree)

#sets up a list showing which tree will go where on which sheet
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
sheet.append(row)
sheets.append(sheet)


#the number of sheets required
noSheets = len(sheets)

#defining the styles for the svg
st0 = ".st0{fill:none;stroke:none;}"
st1 = ".st1{font-family:'Verdana';}"
st2 = ".st2{font-size:1.5mm;}"
circle = ".circle{fill:#000000;}"

styles = [st0, st1, st2, circle]

def get_tree_svg(tree):
	'''takes the filename of an svg tree and returns a group containing that tree which can then be transformed'''

	#get the svg data from the file
	t = open(tree, 'r')
	data = t.read()
	t.close()

	#remove the outer svg tags
	d = data.split('</style>')
	d = d[1][:-6]

	#place the svg data into a group so that the tree can be transformed later on
	group = '<g transform="translate({0} {1}) rotate({2})">\n\t{3}\n</g> {4}'
	group = group.format('{0}', '{1}', '{2}', d, '{3}')

	return group

def create_a_sheet(sheet, styles, sheetx, sheety, location):
	'''converts a sheet list into an svg which can then be lasercut'''

	#getting an svg template from a file
	template = open('svg_template.svg', 'r')
	sheetSVG = template.read()
	template.close()

	#adding the width, height, space for the styles and space for more svg content
	sheetSVG = sheetSVG.format(sheetx, sheety, '{0}', '{1}')

	x = 0
	y = 0
	for row in sheet:
		for tree in row:
			#calculate the transform values
			xTrans = 53.04 * x
			if x % 2 == 0:
				yTrans = 0 + y * (treey + 4)
				rotation = 0
			else:
				xTrans += treex + 0.66
				yTrans = 12.965 + y * (treey + 4)
				yTrans += treey + 0.66
				rotation = 180

			#get the tree SVG
			treeSVG = get_tree_svg(tree)

			#apply the transformation and leave space for a new tree after it
			treeSVG = treeSVG.format(xTrans, yTrans, rotation, '{1}')

			#place the tree on the sheet
			sheetSVG = sheetSVG.format('{0}', treeSVG)
			x += 1
		x = 0
		y += 1

	#add the styles and close the gap
	sheetSVG = sheetSVG.format('\n'.join(styles), '')

	#creates the sheet file
	sheetNo = 0
	failed = True
	while failed:
		try:
			sheetFile = open(location + 'sheet{0}.svg'.format(sheetNo), 'x')
			failed = False
		except:
			sheetNo += 1

	#writes to the sheet file
	sheetFile.write(sheetSVG)
	sheetFile.close()


for sheet in sheets:
	create_a_sheet(sheet, styles, sheetx, sheety, 'sheets_to_engrave/')

	#defining the styles for the svg
	st0 = ".st0{fill:none;stroke:#000000;stroke-miterlimit:10;stroke-width:0.01mm;}"
	st1 = ".st1{font-family:'Verdana';}"
	st2 = ".st2{font-size:1.5mm;fill:none;stroke:#000000;stroke-width:0.01mm;}"
	circle = ".circle{fill:none;stroke:#000000;stroke-width:0.01mm;}"

	styles = [st0, st1, st2, circle]

	create_a_sheet(sheet, styles, sheetx, sheety, 'sheets_to_cut/')



