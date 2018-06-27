import grass.script as grass
import numpy as np
import os

###############################
#  EDIT VALS BELOW THIS LINE  #
###############################

PREFIX = "forest_"  #Map prefix used in the original sim
ELEVPATTERN = 'elevation'  #Name stem for elevation maps.
EDPATTERN = "ED_rate"   #Name stem for ED Rate maps.
DIGITS = 4         #Number of digits in the infixed year number. Will use zfill to pad zeros to this number of digits.
FINALYEAR = 157    #Number of the last year to include in the analysis
INITDEM = "INIT_DEM@forest_1861_2017"  #Full name (with @'mapset') of the initial dem used in the sim
VBMAP = "all_areas@NEW_terrace_digit_2018"  #Full name of the valley bottom map
BASEPATH = '/home/user/Dropbox/research_projects/Bova_Marina/Presentations_and_Pubs/Terrace_changes_2018/Erosion_modeling/Final Runs'
OUTPUTFILE = "%sTERRACE_ERDEP_STATS" % PREFIX  #Name stem for the output stats files. One file will be made for each interval.

###############################
# DO NOT EDIT BELOW THIS LINE #
###############################

#setup the loop, and start looping
###################################

### Regular erdep stats for masked area
print "Calculating yearly ED values for masked area"
namestem = "%s%s*" % (PREFIX, EDPATTERN)
edmaps = grass.read_command('g.list', flags='m', type='rast', pattern=namestem, separator=',').strip().split(',')
statslist = []
rows = np.array(['n cells erosion', 'n cells deposition', 'summed erosion','summed deposition','mean erosion','mean deposition','max erosion','max deposition'], dtype='|S20')
for map1 in edmaps:
    print map1
    grass.mapcalc("${OUT}=if(isnull(${VBMAP}), null(), if(${CUMERDEP} < 0, ${CUMERDEP}, null()))", quiet = 'True', overwrite="True", OUT = "temporary_EROSION_%s_" % map1.split("@")[0], VBMAP = VBMAP, CUMERDEP = map1)
    grass.mapcalc("${OUT}=if(isnull(${VBMAP}), null(), if(${CUMERDEP} > 0, ${CUMERDEP}, null()))", quiet = 'True', overwrite="True", OUT = "temporary_DEPOSITION_%s_" % map1.split("@")[0], VBMAP = VBMAP, CUMERDEP = map1)
    a = grass.parse_command('r.univar', flags = 'g', map = "temporary_EROSION_%s_" % map1.split("@")[0])
    b = grass.parse_command('r.univar', flags = 'g', map = "temporary_DEPOSITION_%s_" % map1.split("@")[0])
    statslist.append([float(a['n']), float(b['n']), float(a['sum']), float(b['sum']), float(a['mean']), float(b['mean']), float(a['min']), float(b['max'])])
grass.run_command("g.remove", type="raster", pattern="temporary_*", flags="f")
statsarray = np.array(statslist)
np.savetxt("%s%s%s.csv" % (BASEPATH, os.sep, OUTPUTFILE), np.vstack((rows, statsarray)), delimiter=",", fmt = "%s")

#Cumulative erdep stats for masked area
print "Calculating cumualtive ED values for masked area"
namestem = "%s%s*" % (PREFIX, ELEVPATTERN)
elevmaps = grass.read_command('g.list', flags='m', type='rast', pattern=namestem, separator=',').strip().split(',')
cumerdeplist = []
for iteration, elevmap in zip(range(FINALYEAR),elevmaps):
    print elevmap
    outname = "%s_cumerdep_%s" % (PREFIX, str(iteration + 1).zfill(DIGITS))
    print outname
    grass.mapcalc("${outname}=(${elevmap} - ${dem})", quiet = 'True', overwrite="True", outname = outname, dem = INITDEM, elevmap = elevmap)
    cumerdeplist.append(outname)
statslist = []
rows = np.array(['n cells erosion', 'n cells deposition', 'summed erosion','summed deposition','mean erosion','mean deposition','max erosion','max deposition'], dtype='|S20')
for map1 in cumerdeplist:
    grass.mapcalc("${OUT}=if(isnull(${VBMAP}), null(), if(${CUMERDEP} < 0, ${CUMERDEP}, null()))", quiet = 'True', overwrite="True", OUT = "temporary_EROSION_%s_" % map1.split("@")[0], VBMAP = VBMAP, CUMERDEP = map1)
    grass.mapcalc("${OUT}=if(isnull(${VBMAP}), null(), if(${CUMERDEP} > 0, ${CUMERDEP}, null()))", quiet = 'True', overwrite="True", OUT = "temporary_DEPOSITION_%s_" % map1.split("@")[0], VBMAP = VBMAP, CUMERDEP = map1)
    a = grass.parse_command('r.univar', flags = 'g', map = "temporary_EROSION_%s_" % map1.split("@")[0])
    b = grass.parse_command('r.univar', flags = 'g', map = "temporary_DEPOSITION_%s_" % map1.split("@")[0])
    statslist.append([float(a['n']), float(b['n']), float(a['sum']), float(b['sum']), float(a['mean']), float(b['mean']), float(a['min']), float(b['max'])])
grass.run_command("g.remove", type="raster", pattern="temporary_*", flags="f")
statsarray = np.array(statslist)
np.savetxt("%s%s%s_cumulative.csv" % (BASEPATH, os.sep, OUTPUTFILE), np.vstack((rows, statsarray)), delimiter=",", fmt = "%s")

print "Finished."

