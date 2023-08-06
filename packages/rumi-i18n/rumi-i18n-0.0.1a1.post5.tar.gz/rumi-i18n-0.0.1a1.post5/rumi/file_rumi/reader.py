# rumi.file_rumi.reader
# Git history reader for file-based translation monitoring
#
# Author: Tianshu Li
# Created: Oct.22 2021

"""
Git history reader for file-based translation monitoring
"""

##########################################################################
# Imports
##########################################################################


import os
import re
import git
import string
import pandas as pd

from io import StringIO
from version import Version

# Language Codes
ALL_LANGS = {
    "aa","ab","ae","af","ak","am","an","ar","as","av","ay","az","ba","be",
    "bg","bh","bm","bi","bn","bo","br","bs","ca","ce","ch","co","cr","cs",
    "cu","cv","cy","da","de","dv","dz","ee","el","en","eo","es","et","eu",
    "fa","ff","fi","fj","fo","fr","fy","ga","gd","gl","gn","gu","gv","ha",
    "he","hi","ho","hr","ht","hu","hy","hz","ia","id","ie","ig","ii","ik",
    "io","is","it","iu","ja","jv","ka","kg","ki","kj","kk","kl","km","kn",
    "ko","kr","ks","ku","kv","kw","ky","la","lb","lg","li","ln","lo","lt",
    "lu","lv","mg","mh","mi","mk","ml","mn","mr","ms","mt","my","na","nb",
    "nd","ne","ng","nl","nn","no","nr","nv","ny","oc","oj","om","or","os",
    "pa","pi","pl","ps","pt","qu","rm","rn","ro","ru","rw","sa","sc","sd",
    "se","sg","si","sk","sl","sm","sn","so","sq","sr","ss","st","su","sv",
    "sw","ta","te","tg","th","ti","tk","tl","tn","to","tr","ts","tt","tw",
    "ty","ug","uk","ur","uz","ve","vi","vo","wa","wo","xh","yi","yo","za",
    "zh","zu"
}


##########################################################################
# Class FileReader
##########################################################################


class FileReader():
    """
    FileReader reads the github history, parses it into a commit dictionary,
    and also parses the source files and source and target languages.

    Parameters
    ----------
    repo_path: string, default: "./"
        Path to the repository for translation monitoring.
    content_path: list of string, default: ["content/"]
        Path from the root of the repository to the directory that contains
        contents that require translation. Default uses the "content/" folder.
    branch: string, default: "main"
        Name of the branch to read the github history from. Default to "main".
    extensions: list of string, default: ["md"]
        Extension of the target files for translation monitoring. Defult
        monitoring translation of the markdown files.
    pattern: string, choices: "folder/", ".lang"
        Two types of patterns in which the static site repository is organized.
    langs: string, default: ""
        Language codes joint by a white space as specified by the user. If not
        specified, GitReader will try to get languages from the filenames in the
        current repository for monitoring.
    src_lang: string, default: "en"
        Default source language set by user.
    """
    def __init__(
        self, repo_url="", repo_path="", branch="main", langs="",
        content_path=["content/"], extensions=["md"], pattern="folder/",
        src_lang = "en"
    ):
        super().__init__(
            content_path=content_path, extensions=extensions, 
            repo_path=repo_path, branch=branch
        )

        self.pattern = pattern
        self.langs = langs
        self.all_langs = ALL_LANGS
        self.src_lang = src_lang

        self.version = Version(self.repo_name)

    def clean_filename(self, filename):
        """
        Clean out the { *** => ***} format in file name
        """
        path_hack = re.search(r'\{.+\}', filename)
        rename_sign = " => "
        if path_hack:
            path_hack = path_hack.group()
            file_name = filename.replace(path_hack, path_hack[1:-1].split("=>")[-1].strip())
        elif rename_sign in filename:
            rename = filename.split(rename_sign)[-1]
            file_name = rename
        return filename

    def read_history(self, start_time):
        """
        Read the git history at the specified branch and preprocess the histories.
        Returns
        -------
        commits: pandas DataFrame
        """
        repo = self.get_repo()

        command = 'git log --numstat --pretty=format:"\t\t\t%h\t%at\t%aN" --since="{}"'.format(start_time)
        git_log = repo.git.execute(command=command, shell=True)

        commits_raw = pd.read_csv(
            StringIO(git_log),
            sep="\t",
            header=None,
            names=['additions', 'deletions', 'filename', 'sha', 'timestamp', 'author']
        )
        commits = commits_raw[['additions', 'deletions', 'filename']]\
            .join(commits_raw[['sha', 'timestamp', 'author']].fillna(method='ffill'))
        commits = commits.dropna()
        return commits

    def parse_history(self, start_time):
        """
        Parse the output from git log command, into a dictionary of file commit
        history.

        Returns
        -------
        commits: dictionary
            Commit history of the repository organized by
            {
                "basename": {
                    "locale": {
                        "filename": name of the target file,
                        "ft": timestamp of the first commit (float),
                        "lt": timestamp of the last commit (float),
                        "history": {
                            timestamp (float): [#additions, #deletions]
                        }
                    },
                    "origin": {
                        source file's locale
                    }
                }
            }
            The basename is the name of the content that is common among languages.
        """
        commits = self.version.load_cache()
        new_commits = self.read_history(self.version.latest_date)

        for i in new_commits.index:
            filename = new_commits.loc[i, "filename"]
            add = new_commits.loc[i, "additions"]
            add = 0 if add == "-" else int(add)
            delete = new_commits.loc[i, "deletions"]
            delete = 0 if delete == "-" else int(delete)

            filename = self.clean_filename(filename)
            if filename in self.targets:
                base_name, lang = self.parse_base_lang(filename)
                if not base_name:
                    continue
                commit_time = float(new_commits.loc[i, "timestamp"])

                if (base_name not in commits):
                    commits[base_name] = {}

                if filename in commits[base_name]:
                    if commit_time < commits[base_name][lang]["ft"]:
                        commits[base_name][lang]["ft"] = commit_time
                    elif commit_time > commits[base_name][lang]["lt"]:
                        commits[base_name][lang]["lt"] = commit_time

                    commits[base_name][lang]["history"][commit_time] = [add, delete]
                else:
                    commits[base_name][lang] = {
                        "filename": filename,
                        "ft": commit_time,
                        "lt": commit_time,
                        "history": {
                            commit_time: [add, delete]
                        }
                    }

        self.version.write_cache(commits)

        commits = self.set_langs(commits)
        commits = self.set_origins(commits)
        return commits

    def parse_base_lang(self, file_name):
        """
        Given a full path/to/file/filename, parse the basename and langauge with
        consideration of the two types of repository organization patterns: "folder/"
        and ".lang".

        Parameters
        ----------
        file_name: string
            Name of the file.

        Returns
        -------
        basename: string
            Name of the file content that remains unchanged among languages.

        lang: string
            Code of language used in the file.
        """
        base_name, lang = None, None
        if self.pattern == "folder/":
            for split in file_name.split("/"):
                if split in self.all_langs:
                    lang = split
                    base_name = os.path.basename(file_name)
                    break
        elif self.pattern == ".lang":
            lang = file_name.split(".")[-2]
            assert lang in self.all_langs, "Invalid format of translation files"
            base_name = file_name.replace("."+lang, "")
        return base_name, lang

    def get_langs(self, commits):
        """
        User can define the target languages to monitor for translation
        by providing a string e.g. "en fr zh de". If the target langauges
        are not provided, the get_langs function will get langauges based
        on the file names and the ALL_LANGS set.

        Returns
        -------
        langs: set
            Set of all language codes contained and monitored in the repository.
        """
        if self.langs != "":
            # Verify the specified language string is valid
            allowed = set(string.ascii_lowercase + string.whitespace)
            assert set(self.langs) <= allowed, "Invalid languages specified. Only lowercase letters and whitespace are allowed"
            return set(self.langs.split(" "))
        else:
            langs = []
            for base_file in commits:
                for file in commits[base_file]:
                    langs.append(commits[base_file][file]["lang"])
            return set(langs)

    def set_langs(self, commits):
        """
        Parse through the commit dictionary and set all langs.
        """
        for basefile in commits:
            files = commits[basefile]
            for lang in self.get_langs(commits):
                if lang not in files:
                    files[lang] = {}
        return commits

    def set_origins(self, commits):
        """
        Parse through the commit dictionary and set all source files.
        """
        for base_file in commits:
            st = float('inf')
            for lang in commits[base_file]:
                file_dict = commits[base_file][lang]
                if file_dict["ft"] < st:
                    commits[base_file]["origin"] = lang
                    st = file_dict["ft"]
                elif file_dict["ft"] == st:
                    if lang == self.src_lang:
                        commits[base_file]["origin"] = lang
        return commits
    
    def add_target(self, filename):
        """
        Allow user to add single target file that are not captured by 
        content_path and target file extension.
        """
        for path2file in self.repo_set:
            basename = os.path.basename(path2file)
            if filename == basename:
                self.targets.add(path2file)
                return
        print("Please provide a valid file name")
        return

    def del_target(self, filename):
        """
        Allow user to delete single target file.
        """
        for path2file in self.repo_set:
            basename = os.path.basename(path2file)
            if filename == basename:
                self.targets.remove(path2file)
                return
        print("Please provide a valid file name")
        return