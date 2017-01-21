OS-Based Jupyterlab Collaboration RFC
--------------------------------------

## Overview
The overview of this RFC is to provide a lightweight, low-dependency
system for allowing a multi-member team to collaborate on large-scale
data analysis using a combination of JupyerLab and other data science tools.

## Technical Roadmap (rough notes)

### Multi-user env on remote instance

* Use the same conda at ec2-user/anaconda/...conda for staring jupyterlab
* Create multiple ec2 users for each person on the team
* Nice side-effect of this is that they have their own pem file
    * Can we use aws-cli to download the pem  file for them (?
    * Also - look into a secure way to distribute a pem file
    * For each ecc2 user, separate jupyter lab notebook dir
        * Plus a symlink to th shared drive
    * Using UNIX permissions people won't be able to access others work
    * TODO: investigate jupyerlab's behavior on opening a file that it doesnt have perms for

### Sahring mechanism

* Shared python bins available on all users path (fabricator script to add
  that from ec2-user/bin)
* Proposed syntax "./share <nb_username> <nb/path>"
* What this does is it will create a shared directory (new dir) that you both have perms to edit
    * The shared directory will have a unique id
    * This will alboe have a collaboration number for a more acaademicy-sense: Nb_Name:version
* They can both work on it (old schol shitty ipython collab)
* Command syntax structure for a "shared collab id" will be either <shared_collab_id> 
  or <author_id1,.,author_idk>:collaboration_nb_name> 

### Publishing
* The ./publish command
    * From any notebook directory that is a "finalized" the file name should be prepended "_FINAL"
    * If it is a notebook that has been published before, the absence of a version string should
      be incremented as a <MINOR> version in the publish to the "blessed" directory
        = The "versioning" convention is as follows:
            * Incremeting a MAJOR version if it includes breaking changes, significant
              product pivots or a whole redesign
            * MINOR versions signify code that is an incremental, non-breaking addition that has new features
            * HOTFIX versions signify minor changes or bugfixes
   * The syntax of the publish command is 
       * './publish <shared_collab_id> -version <MAJOR|MINOR|HOTFIX> -- NotebookName'


### Other Thoughts

* Would like to make this backed by git (which then can be incrementally backed up/serialized to s3 bucket)
* Branching semantics (for when we eventually hook in git)
* Git specificts for this would be "./publish" executing merging back to the master of the shared nb dir
    * Other git thoughts for shared collaboration - the shared dir could be grouped with the master
      branch, or a spearate jupyterlab instance on the master user for "collaboration"
* For publication, have some notion of a "project" (that has some metadata file linking to an asana tak)
* Need to figure out a good distribution mechanism for the AWS keys to log on to the box
