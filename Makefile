help:
	@echo "    test"
	@echo "        Run some tests"
	@echo "    install"
	@echo "        Install for local development"

test:
	rm -rf tmp
	mkdir tmp
	@echo "Generating some large files.."
	dd if=/dev/random of=tmp/large_binary.bin bs=1M count=122
	dd if=/dev/random of=tmp/large_nii.nii.gz bs=1M count=230
	dd if=/dev/random of=tmp/large_txt.txt bs=1M count=111
	ls -lah tmp
	@echo "Storing checksums"
	md5sum -b tmp/large_* > tmp/checksums
	@echo "Splitting .bin larger than 100M in chunks of 10M"
	ghsplit --root=tmp split --max-size=100 --extension=.bin --chunk-size=10
	ls -lah tmp
	@echo "Splitting .nii.gz larger than 200M in chunks of 50M"
	ghsplit --root=tmp split --max-size=200 --extension=.nii.gz --chunk-size=50
	ls -lah tmp
	@echo "Splitting any file larger than 99M in chunks of 50M"
	ghsplit --root=tmp split
	ls -lah tmp
	@echo "Merge everything back"
	ghsplit --root=tmp merge
	ls -lah tmp
	@echo "Verifying checksums"
	md5sum -c tmp/checksums

clean:
	rm -rf ./*.egg-info
	rm -rf tmp

install: clean
	pip install --user -e .
