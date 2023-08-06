RSYNC=rsync -zzcav \
	--exclude=\*~ --exclude=.\* \
	--delete-excluded --delete-after \
	--no-owner --no-group \
	--progress --stats


doc: .sphinx-stamp

doc-upload:
	$(RSYNC) build/doc/ dcmod.org:~/public_html/geotiler

.sphinx-stamp: .map-stamp
	PYTHONPATH=. sphinx-build doc build/doc

.map-stamp:
	PYTHONPATH=. ./bin/geotiler-lint --cache redis -c -6.069 53.390 -s 512 512 -z 15 doc/map-osm.png
	PYTHONPATH=. ./bin/geotiler-lint --cache redis -c -6.069 53.390 -s 512 512 -z 15 -p stamen-toner doc/map-stamen-toner.png
	PYTHONPATH=. ./bin/geotiler-lint --cache redis -c -6.069 53.390 -z 8 -s 512 512 -p bluemarble doc/map-bluemarble.png
	PYTHONPATH=. ./bin/geotiler-route -r 5 -a 1 --cache redis data/path.gpx doc/map-path.png
