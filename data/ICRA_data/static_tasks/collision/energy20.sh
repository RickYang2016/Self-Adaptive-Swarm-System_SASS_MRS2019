cd 20/

for dir in `ls .`
do
	if [ -d $dir ];
	then
		cd $dir/
		for((i=1;i<=20;i++))
		do
		    cat 2019-08-?????????$i.log | grep Energy | cut -f2 -d']' > a
		    tail -n +9  a > energy$i.txt
		    rm a
		done

		for((i=1;i<=20;i++))
		do
		    cat 2019-08-?????????$i.log | grep Walk | cut -f4 -d' ' > walk$i.txt
		done

		for((i=1;i<=20;i++))
		do
		    cat 2019-08-?????????$i.log | grep Walk | cut -f2 -d' ' | cut -f1 -d':' > time$i.txt
		done

		paste time3.txt energy*.txt > time_energy.txt

		paste time3.txt walk*.txt > time_walk.txt

		cd ../
	fi
done