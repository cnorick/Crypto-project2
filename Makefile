all:
	# Move executables to this directory and remove thier '.sh' suffix.
	cp bash_scripts/rsa-dec.sh rsa-dec
	cp bash_scripts/rsa-enc.sh rsa-enc
	cp bash_scripts/rsa-keygen.sh rsa-keygen

	# Change permission on files to allow execution
	chmod a+x rsa-dec
	chmod a+x rsa-enc
	chmod a+x rsa-keygen

clean:
	rm rsa-dec rsa-enc rsa-keygen