#!/bin/bash

#  _____ _____ ____ _____   _____    _    ____ _   _    ____ ___  ____  _____ 
# |_   _| ____/ ___|_   _| | ____|  / \  / ___| | | |  / ___/ _ \|  _ \| ____|
#   | | |  _| \___ \ | |   |  _|   / _ \| |   | |_| | | |  | | | | | | |  _|  
#   | | | |___ ___) || |   | |___ / ___ \ |___|  _  | | |__| |_| | |_| | |___ 
#   |_| |_____|____/ |_|   |_____/_/   \_\____|_| |_|  \____\___/|____/|_____|
#                                                                            

_args_=($@) # all parameters from terminal.
printf "args\n\t${_args_[*]}\n"

# tools check
_t_satisfied_=true
_t_is_n_i_="is not installed"
for t in curl sha256sum
do
    if ! [[ -x $(which $t) ]]; then
        _t_satisfied_=false
        echo "> $t"
    fi
done
if ! $_t_satisfied_; then
    echo "The above is/are not installed, getcodium exit."
    exit
fi

# print mirrors
print_mirrors(){
    printf "\ncat ${PWD}/codium.mirrors\n"
    cat ${PWD}/codium.mirrors
}

# print help
if [[ ${_args_} == -h ]] ; then
    printf "use 'getcodium [mirror_name]' to install codium"
    print_mirrors
    exit
fi

# get pkg_extension
_release_id_=$(cat /etc/os-release | grep -Eo  '^ID=(\S*)')
_release_id_=${_release_id_:3}
################################################################################
_pkg_ext_=$([[ 'ubuntu debian' == *${_release_id_}* ]] && echo "deb" || \
    echo "deb")
################################################################################
printf "pkg_ext\n\t${_pkg_ext_}\n"


################################################################################
# is debian?
[[ $_pkg_ext_ == 'deb' ]] && _is_debian_=true || _is_debian_=false
printf "is_debian\n\t"; $is_debian && printf 'Y' || printf 'N'; printf "\n"
################################################################################

# get_kernel
_kernel_=$(echo `uname -s` | tr '[:upper:]' '[:lower:]')
printf "kernel\n\t${_kernel_}\n"

# get processor
_processor_=$(echo `uname -p` | tr '[:upper:]' '[:lower:]')
################################################################################
if [[ $_kernel_ == 'linux' ]]; then
    if [[ 'x86_64 amd64' == *${_processor_}* ]]; then
        _processor_="amd64"
    elif [[ 'aarch64 arm64' == *${_processor_}* ]] && $_is_debian_; then
        _processor_="arm64"
    # elif
    fi
# elif
fi
################################################################################
printf "processor\n\t${_processor_}\n"

# specified mirror
_mirror_='BFSU'
if [[ -n ${_args_} ]]; then
    if  [[ "$(cat codium.mirrors)" == *${_args_}\ * ]]; then
        _mirror_="${_args_}"
    else
        echo "The mirror has been reset, the recorded mirror is following:"
        print_mirrors
    fi
fi
printf "mirror\n\t${_mirror_}\n"

# get mirror url
_mirror_url_=$(cat codium.mirrors | grep ${_mirror_})
_mirror_url_=(${_mirror_url_})
_mirror_url_=${_mirror_url_[1]}
printf "mirror_url\n\t${_mirror_url_}\n"

# download pkg
_pkg_name_=$(curl $_mirror_url_ | grep $_processor_ | \
    grep -Eo ">\S*.$_pkg_ext_<")
_pkg_name_=${_pkg_name_:1:-1}
[[ $_pkg_name_ == */* ]] && return
echo "download ${_pkg_name_} . . ."
curl $_mirror_url_$_pkg_name_ -o $_pkg_name_

# download pkg sha256
_pkgsha256_name_=$(curl $_mirror_url_ | grep $_processor_ | \
    grep -Eo ">\S*.${_pkg_ext_}.sha256<")
_pkgsha256_name_=${_pkgsha256_name_:1:-1}
[[ $_pkgsha256_name_ == */* ]] && return
echo "download ${_pkgsha256_name_} . . ."
curl $_mirror_url_$_pkgsha256_name_ -o $_pkgsha256_name_

# sha256sum check and install codium
_sha256sum_check_=$(cat $_pkgsha256_name_ | sha256sum --check | \
    tr '[:upper:]' '[:lower:]')
if [[ $_sha256sum_check_ == *ok ]]; then
################################################################################
    if $_is_debian_; then
        printf "\nsudo dpkg --install $_pkg_name_\n\n"
        sudo dpkg --install $_pkg_name_
        [[ $_pkg_name_ == */* ]] && echo "getcodium crashs, exit." && \
        return
        [[ $_pkgsha256_name_ == */* ]] && echo "getcodium crashs, exit." && \
        return
        rm -rf $_pkg_name_ $_pkgsha256_name_
    # elif true; then
    fi
################################################################################
    echo "codium is installed. HAPPY CODING :-) "
else
    echo "sha256sum checking failed! getcodium exit."
fi

# wait for you to contribute the code.
