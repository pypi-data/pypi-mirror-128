# rumi.file_rumi.reporter
# Reporter for file-based translation monitoring
#
# Author: Tianshu Li
# Created: Oct.22 2021

"""
Reporter for file-based translation monitoring
"""

##########################################################################
# Imports
##########################################################################


from tabulate import tabulate

from rumi.file_rumi.reader import GitReader


##########################################################################
# Class FileReporter
##########################################################################


class FileReporter():
    """
    The FileReporter can display the translation status of the static 
    site repository in two modes:
    1. stats mode: displays the number of Open (hasn't been translated), 
    Updated (source file has been updated after translation), Completed 
    (source file has been translated for all target languages). E.g.:
        | Language   |   Total  |   Open |   Updated |   Completed |
        |------------+----------+--------+-----------+-------------|
        | fr         |        0 |      0 |         0 |           0 |
        | en         |       17 |     12 |         1 |           4 |
        | zh         |        0 |      0 |         0 |           0 |
    2. detail mode: displays translation work required for each source file
    together with the word count. E.g.:
        | File  | Status | Source Language | Target Language | Word Count| Percent Change|
        |-------+--------+-----------------+-----------------+-----------+---------------|
        | file1 | Update | en              | zh              | ?         | 50%           |
        | file2 | Open   | en              | fr              | 404       | 100%          |
        | file3 | Open   | en              | zh              | 404       | 100%          |
    
    Parameters
    ----------
    repo_path: string, default: "./"
        Path to the repository to monitory the translation status. Default
        uses the current path. 
    
    src_lang: string, default: ""
        Language code of the source language (the original language of 
        contents) to be monitored. If not specified, all source language 
        will be monitored.
    
    tgt_lang: string, default: ""
        Language code of the target language (language to translate contents
        into) to be monitored. If not specified, all target language will 
        be monitored.
    """
    def __init__(self, repo_path="./", src_lang="", tgt_lang=""):
        self.repo_path = repo_path
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang

    def set_stats(self, commits):
        """
        Set the translation stats of Total (number of target files), Open (
        hasn't been translated), Updated (has been changed since translation), 
        and completed.

        Parameters
        ----------
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
                        },
                        "status": {
                            "open", "updated", "completed", or "source"
                        }
                    },
                    "origin": {
                        source file's locale
                    }
                }
            }
        """

        for basefile in commits:
            files = commits[basefile]
            for lang in files:
                src_lang = files["origin"]
                if lang == src_lang:
                    files[lang]["status"] = "source"
                else:
                    if files[lang] == {}:
                        files[lang]["status"] = "open"
                    elif files[lang]["lt"] > files[src_lang]["lt"]:
                        files[lang]["status"] = "completed"
                    elif files[lang]["lt"] < files[src_lang]["lt"]:
                        files[lang]["status"] = "updated"
                    elif files[lang]["lt"] == files[src_lang]["lt"]:
                        # When source and target file were changed in the same
                        # commit but source file has more cumulative additions, 
                        # the status is also marked as updated.
                        tgt_add = sum(change[0] for change in files[lang]["history"])
                        src_add = sum(change[0] for change in files[src_lang]["history"])
                        if (tgt_add < src_add):
                            files[lang]["status"] = "updated"
                        else:
                            files[lang]["status"] = "completed"

    def get_stats(self, commits):
        """
        Set the translation stats from commit history after setting status.

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
                        },
                        "status": {
                            "open", "updated", "completed", or "source"
                        }
                    },
                    "origin": {
                        source file's locale
                    }
                }
            }
        
        Returns
        -------
        stats: dictionary
            {
                locale: {
                    "total": int, 
                    "open": int, 
                    "updated": int,
                    "completed": int
                }
            }
        """
        stats = {}

        for basefile in commits:
            files = commits[basefile]
            for lang in files:
                status = files[lang]["status"]
                if status != "source":
                    stats[lang]["total"] += 1
                    stats[lang][status] += 1
        return stats

    def stats(self, stats):
        """
        Print out a summary of the translation status.

        Parameters
        ----------
        stats: dictionary
            {
                locale: {
                    "total": int, 
                    "open": int, 
                    "updated": int,
                    "completed": int
                }
            }
        """
        data = []
        for lang in stats:
            stat = stats[lang]
            data.append([
                lang, stat["total"], stat["open"], stat["updated"], stat["completed"]
            ])

        print(tabulate(
            data, 
            headers=["Target Language", "Total", "Open", "Updated", "Completed"],
            tablefmt="orgtbl"
        ))
    
    def get_details(self, commits):
        """
        Get details of translation needs containing File (source filename), Status 
        (Open, Updated, or Completed), Source Language, Target Language, Word 
        Count, and Percent Change.

        Returns
        -------
        details: list
            [{
                "basefile": name of the source file
                "status": "open" or "updated",
                "src_lang": source language,
                "tgt_lang": target language,
                "wc": word count, 
                "pc": percent change
            }]
        """
        details = []
        for basefile in commits:
            files = commits[basefile]
            src_lang = files["origin"]
            wc = self.word_count(basefile)
            n_lines = self.count_lines(files[src_lang]["filename"])
            for lang in files:
                status = files[lang]["status"]
                if status == "open":
                    pc = "100%"
                elif status == "updated":
                    tgt_lt = files[lang]["lt"]
                    n_additions = self.count_additions(files[src_lang]["history"], tgt_lt)
                    pc = str(round(n_additions / n_lines, 3) * 100)+"%"
                else:
                    continue
                
                details.append({
                    "basefile": basefile,
                    "status": status,
                    "src_lang": src_lang,
                    "tgt_lang": lang,
                    "wc": wc, 
                    "pc": pc
                })
        return details

    def detail(self, details):
        """
        Print out the details of the work required for translating each source
        file, its Open/Update status, source and target language, and the count
        of words in the source file.
        """
        data = []
        for row in details:
            if (
                (self.src_lang=="" or self.src_lang==row["src_lang"]) and 
                (self.tgt_lang=="" or self.tgt_lang==row["tgt_lang"])
            ):

                data.append([
                    row["basefile"], row["status"], row["src_lang"], 
                    row["tgt_lang"], row["wc"], row["pc"]
                ])
        # Print detail data in tabulate format
        print(tabulate(
            data, 
            headers=["Source File", "Status", "Source Language", "Target Language", "Word Count", "Percent Change"],
            tablefmt='orgtbl'
        ))

    def word_count(self, file):
        """
        Estimate the word count of a given file.
        
        Parameters
        ----------
        file: string
            Name of the file.
        
        Returns
        -------
        wc: int
            Estimation of word count.
        """
        wc = 0
        with open(self.repo_path+file, "r+") as f:
            for line in f:
                wc += len(line.split(" "))
        return wc

    def count_lines(self, file):
        """
        Count the total number of lines of a given file.

        Parameters
        ----------
        file: string
            Name of the file.
        
        Returns
        -------
        cnt: int
            Number of lines
        """
        with open(self.repo_path+file, "r+") as f:
            cnt = len(f.readlines())
        return cnt

    def count_additions(self, src_file, tgt_file):
        """
        Count the number of additions in tgt_file maintained by git history
        after src_file's last commit.

        Parameters
        ----------
        src_file: dictionary
            Commit history of the source file: 
            {
                "filename": name of the target file,
                "ft": timestamp of the first commit (float),
                "lt": timestamp of the last commit (float),
                "history": {
                    timestamp (float): [#additions, #deletions]
                },
                "status": {
                    "open", "updated", "completed", or "source"
            }
        
        tgt_history: dictionary
            Commit history of the target file.
        
        Returns
        -------
        cnt: int
            Total number of additions after timestamp.
        """
        src_lt, tgt_lt = src_file["lt"], tgt_file["lt"]
        
        if tgt_lt < src_lt:
            # Count all additions in the origin file after current file's last update timestamp
            cnt = 0
            for ts in src_file["history"]:
                if ts > tgt_lt:
                    cnt += src_file["history"][ts][0]
        elif tgt_lt == src_lt:
            # When source and target file were changed in the same
            # commit but source file has more additions, the status
            # is also marked as updated.
            tgt_add = sum(change[0] for change in files[lang]["history"])
            src_add = sum(change[0] for change in files[src_lang]["history"])
            assert src_add > tgt_add
            cnt = src_add - tgt_add
        return cnt