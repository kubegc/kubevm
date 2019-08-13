
# Prepare environment

* Softwares needed for kubevmm commands:
    ```
    docker
    ```

*  Same `version` of docker images in remote repository.
    ```
    registry.cn-hangzhou.aliyuncs.com/cloudplus-lab
    ```

# Build

## Manual

Build the RPM as a non-root user from your home directory:

* Check out this repo. Seriously - check it out. Nice.
    ```
    cd $HOME
    git clone <this_repo_url>
    ```

* Install `rpmdevtools`.
    ```
    sudo yum install rpmdevtools
    ```

* Install `pyinstaller`.
    ```
    sudo pip install pyinstaller
    ```

* Set up your `rpmbuild` directory tree.
    ```
    rpmdev-setuptree
    ```

* Execute `pyinstaller` to build `SOURCES`.
    ```
    cd $HOME/kubevmm/executor
    pyinstaller -F $HOME/kubevmm/executor/kubevmm_adm.py -n kubevmm-adm
    pyinstaller -F $HOME/kubevmm/executor/vmm.py
    
    ```

* Link the spec file and sources.
    ```
    ln -s $HOME/kubevmm/executor/SPECS/kubevmm.spec $HOME/rpmbuild/SPECS/
    find $HOME/kubevmm/executor/dist -type f -exec ln -s {} $HOME/rpmbuild/SOURCES/ \;
    ```
    
* Build the RPM.

    #### Version
    
    The version number is hardcoded into the SPEC, however should you so choose, it can be set explicitly by passing an argument to `rpmbuild` directly:

    ```
    rpmbuild -ba $HOME/rpmbuild/SPECS/kubevmm.spec --define "_version v0.9.0"
    ```
    

# Result

RPMs:
- kubevmm

# Install

## Install online

* Install `kubevmm` rpm.

* Verify `kubevmm`.

  There are two commands: `kubevmm-adm` and `vmm`
    ```
    kubevmm-adm --version
    vmm
    ```

* Pull docker images.

   **Note!** Need same `version` of docker images in remote repository.
    ```
    export KUBEVMM_VERSION=`kubevmm-adm --version`
    docker pull registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtctl:$KUBEVMM_VERSION
    docker pull registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-virtlet:$KUBEVMM_VERSION
    ```
    
# Run

* Run services.
    ```
    kubevmm-adm service start
    ```

* Check services status.
    ```
    kubevmm-adm service status
    ```
