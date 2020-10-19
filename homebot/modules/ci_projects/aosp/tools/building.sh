#!/bin/bash

bot_dir=$(pwd)

# Parse arguments passed by the ROM or recovery's script
while [ "${#}" -gt 0 ]; do
	case "${1}" in
		--project )
			CI_AOSP_PROJECT="${2}"
			shift
			;;
		--name )
			CI_AOSP_PROJECT_NAME="${2}"
			shift
			;;
		--version )
			CI_AOSP_PROJECT_VERSION="${2}"
			shift
			;;
		--lunch_prefix )
			CI_LUNCH_PREFIX="${2}"
			shift
			;;
		--lunch_suffix )
			CI_LUNCH_SUFFIX="${2}"
			shift
			;;
		--build_target )
			CI_BUILD_TARGET="${2}"
			shift
			;;
		--artifacts )
			CI_OUT_ARTIFACTS_NAME="${2}"
			shift
			;;
		--clean )
			CI_CLEAN=clean
			;;
		--installclean )
			CI_CLEAN=installclean
			;;
		--device )
			CI_DEVICE="${2}"
			shift
			;;
		--main_dir )
			CI_MAIN_DIR="${2}"
			shift
			;;
	esac
	shift
done

if [ "$CI_DEVICE" = "" ] || [ ! -d "$CI_MAIN_DIR/$CI_AOSP_PROJECT" ]; then
	exit 4
fi

cd "${CI_MAIN_DIR}/${CI_AOSP_PROJECT}"
. build/envsetup.sh

lunch ${CI_LUNCH_PREFIX}_${CI_DEVICE}-${CI_LUNCH_SUFFIX} &> lunch_log.txt
CI_LUNCH_STATUS=$?
if [ $CI_LUNCH_STATUS != 0 ]; then
	CI_BUILD_END=$(date +"%s")
	CI_BUILD_DURATION=$(( CI_BUILD_END - CI_BUILD_START ))
	exit 5
fi

if [ "$CI_CLEAN" != "" ]; then
	mka $CI_CLEAN &> clean_log.txt
	CI_CLEAN_STATUS=$?
	if [ $CI_CLEAN_STATUS != 0 ]; then
		CI_BUILD_END=$(date +"%s")
		CI_BUILD_DURATION=$(( CI_BUILD_END - CI_BUILD_START ))
		exit 6
	fi
fi

mka $CI_BUILD_TARGET -j$(nproc --all) &> build_log.txt
CI_BUILD_STATUS=$?
if [ $CI_BUILD_STATUS != 0 ]; then
	CI_BUILD_END=$(date +"%s")
	CI_BUILD_DURATION=$(( CI_BUILD_END - CI_BUILD_START ))
	exit 7
fi

CI_BUILD_END=$(date +"%s")
CI_BUILD_DURATION=$(( CI_BUILD_END - CI_BUILD_START ))

exit 0
