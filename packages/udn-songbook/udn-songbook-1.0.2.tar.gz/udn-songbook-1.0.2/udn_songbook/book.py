#!/usr/bin/env python3
# vim: set ts=4 sts=4 sw=4 et ci nu ft=python:

import os
import fnmatch
# from glob import glob

# from jinja2 import Environment, FileSystemLoader

from . import song
from collections import OrderedDict
from operator import attrgetter, itemgetter


class SongBook(object):
    """
    wrapper around a list of songs with additional context
    provides stylesheets, template environments, indexing etc
    """

    def __init__(self, inputs=[], stylesheets=[], duplicates=False):
        """
        Create a songbook object from a list of inputs.
        Inputs can be directories, too.
        By default, songbook content is just a list, so can have
        repeat entries.

        Kwargs:
            inputs(list[str]): list of files or directories containing UDN files
            stylesheets(list[str]): CSS stylesheets to use for rendering the book
            duplicates(bool): Whether to allow duplicate title/artist songs in the book.
        """
        self._inputs = inputs
        self._stylesheets = stylesheets
        # keep track of all the chord diagrams we need for the book
        self.chords = set([])
        self.contents = []
        # index will actually be { title artist: [ list of songs ] }
        self._index = {}

        if len(self._inputs):
            self.populate()
            self.collate()

    def add_song(self, path):
        """
        add a song to the contents list and index

        Args:
            songdata(str): path to a file (usually)
        """
        try:
            s = song.Song(path)
            # add the song object to our content list
            self.contents.append(s)
            # add the chords it uses to our chords list
            self.chords.update(s.chords)
            # insert into index
            if s.songid not in self._index:
                self._index[s.songid] = []
            self._index[s.songid].append(s)
            print(self._index)
        except:
            print("failed to add song", path)
            raise

    def populate(self):
        """
        Reads in the content of any input directories, as Song objects
        """
        for src in self._inputs:
            if os.path.exists(src):
                rp = os.path.realpath(src)
                if (os.path.isfile(rp) and
                   fnmatch.fnmatch(os.path.basename(rp), "*.udn")):
                    print("adding songfile {}".format(rp))
                    self.add_song(rp)
                    continue
                if os.path.isdir(rp):
                    print("Scanning dir {} for ukedown files".format(rp))
                    for rt, dirs, files in os.walk(rp):
                        for f in fnmatch.filter(
                                [os.path.join(rt, f)for f in files], "*.udn"):
                            self.add_song(f)
            else:
                print("cannot load from non-file/dir {}".format(src))

        # self.chords.update(set(s.chords) for s in self.contents)
        # print(self.contents)
        # print([s.chords for s in self.contents])
        # self.chords = set(s.chords for s in self.contents)

    def collate(self):
        """
        reduce contents list to unique entries, indexed on title - artist
        title and artist must be a unique combination.
        Although we could permit dupes I guess, depending on the book.
        """
        return OrderedDict({k: s for (k, v) in
                            sorted(self._index.items(), key=itemgetter(0))
                            for s in v})

    def add(self, songfile):
        """Add a new song to the book

        Adds a new song object to the current songbook

        Args:
            songfile (str): path to songfile
        """
        pass

    def update(self, inputs):
        """
        replace entires in an existing songbook using the provided inputs
        This will regenerate the index
        """
        pass

    def refresh(self):
        """
        reload all the current inputs (that have changed)
        This is a checksumming/stat operation
        """
        # walk over current index/contents
        # check stat for last change (since songbook population)
        # compare checksum - has the content actually changed?
        # this is a PATH operation and may rebuild the songbook index
        # this permits us to change metadata (title etc) and have the book
        # reordered appropriately.
        pass

    def render(self, template):
        # renders the songbook to a file or files.
        pass

    @property
    def inputs(self):
        return self._inputs

    @property
    def index(self):
        return self._index

