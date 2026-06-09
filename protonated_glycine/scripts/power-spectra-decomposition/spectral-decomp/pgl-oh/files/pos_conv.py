

natoms = 14
nframes = 125000 
nmon_atoms = 11
nwaters = 1
timestep = 0.0001
order = ['OG','HG']
#order = ['NG','HG','HG','HG','CG','HG','HG','CG','OG','OG','HG']
#wat_order = ['OW','HW','HW']


def read_file(fname):
	f = open(fname, 'r+')
	frames = []
	mon_frames = []
	box_tot = []
	for i in range(nframes):
#		waters = []
		mon = []
		box = []
		f.readline()
		timestep = int(f.readline())
		box.append(timestep)
		for k in range(3):
			f.readline()
		for j in range(3):
			coord = f.readline().split()
#			box.append(abs(float(coord[0])) + float(coord[1]))
		box_tot.append(box)
		f.readline()
		mon = []
		for n in range(9):
			f.readline()
		for m in range(2):
			monline = f.readline().split()
			monline = monline[4:7]
			monline.insert(0, order[m])
			newmon = ' '.join(monline)
			newmon += '\n'
			mon.append(newmon)
		mon_frames.append(mon)
#		for p in range(2):
#			f.readline()
		for j in range(natoms - nmon_atoms):
			line = f.readline().split()
#			line = line[4:]
#			line.insert(0, wat_order[j % 3])
#			newline = ' '.join(line)
#			newline += "\n"
#			waters.append(newline)	
#		frames.append(waters)
	#print(frames)
	#print(mon_frames)
	#print(box_tot)
	return mon_frames, box_tot
	#return frames, mon_frames, box_tot




def write_file(fname, mon_frames, box_tot):
#def write_file(fname, frames, mon_frames, box_tot):
	f1 = open(fname, 'w+')
	for i in range(nframes):
		f1.write('	' + str(box_tot[i][0]) + '	' + str(timestep * box_tot[i][0]) + '      ' + str(2) + '\n')
#		f1.write(str(box_tot[i][1]) + '      ' + '0.0' + '      ' + '0.0' + '\n')
#		f1.write('0.0' + '      ' + str(box_tot[i][2]) + '      ' + '0.0' + '\n')
#		f1.write('0.0' + '      ' + '0.0' + '      ' + str(box_tot[i][3]) + '\n')
		for k in range(2):
			f1.write(mon_frames[i][k])
#		for j in range(natoms - nmon_atoms):
#			f1.write(frames[i][j])	


mon_frames, box_tot = read_file('dump.lammpstrj')
write_file('VELOCITY_CMD', mon_frames, box_tot)

