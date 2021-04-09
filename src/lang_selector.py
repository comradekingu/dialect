# Copyright 2020-2021 Mufeed Ali
# Copyright 2020-2021 Rafael Mardojai CM
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from gi.repository import Gio, GObject, Gtk

from dialect.define import RES_PATH


@Gtk.Template(resource_path=f'{RES_PATH}/lang-selector.ui')
class DialectLangSelector(Gtk.Popover):
    __gtype_name__ = 'DialectLangSelector'

    # Get widgets
    search = Gtk.Template.Child()
    scroll = Gtk.Template.Child()
    revealer = Gtk.Template.Child()
    recent_list = Gtk.Template.Child()
    separator = Gtk.Template.Child()
    lang_list = Gtk.Template.Child()

    # Propeties
    selected = GObject.Property(type=str)  # Key of the selected lang

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Connect popover closed signal
        self.connect('closed', self._closed)
        # Connect list signals
        self.recent_list.connect('row-activated', self._activated)
        self.lang_list.connect('row-activated', self._activated)
        # Connect search entry changed signal
        self.search.connect('changed', self._update_search)

        self.recent_model = Gio.ListStore.new(LangObject)
        self.recent_list.bind_model(self.recent_model, self._create_lang_row)

        self.lang_model = Gio.ListStore.new(LangObject)
        self.lang_list.bind_model(self.lang_model, self._create_lang_row)

    def set_languages(self, languages):
        # Clear list
        self.lang_model.remove_all()

        # Load langs list
        for code, name in languages.items():
            row_selected = (code == self.selected)
            self.lang_model.append(LangObject(code, name.capitalize(), row_selected))

    def insert_recent(self, code, name):
        row_selected = (code == self.selected)
        self.recent_model.append(LangObject(code, name, row_selected))

    def clear_recent(self):
        self.recent_model.remove_all()

    def refresh_selected(self):
        for lang in self.lang_list:
            lang.selected = (lang.code == self.selected)

    def _activated(self, _list, row):
        # Close popover
        self.popdown()
        # Set selected property
        self.set_property('selected', row.code)

    def _closed(self, _popover):
        # Reset scroll
        vscroll = self.scroll.get_vadjustment()
        vscroll.set_value(0)
        # Clear search
        self.search.set_text('')

    @staticmethod
    def _create_lang_row(lang_object):
        return LangRow(lang_object.code, lang_object.name, lang_object.selected, lang_object.visible)

    def _filter_func(self):
        search = self.search.get_text().lower()
        for object in self.lang_model:
            if object.name.lower().startswith(search) or object.code.lower().startswith(search):
                object.visible = True
            else:
                object.visible = False
        self.lang_model.items_changed(0, len(self.lang_model), len(self.lang_model))

    def _update_search(self, _entry):
        search = self.search.get_text()
        if search != '':
            self.revealer.set_reveal_child(False)
        else:
            self.revealer.set_reveal_child(True)
        self._filter_func()


class LangRow(Gtk.ListBoxRow):

    def __init__(self, code, name, selected=False, visible=True, **kwargs):
        super().__init__(**kwargs)

        self.code = code
        self.name = name

        row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        label = Gtk.Label()
        label.set_text(self.name)
        label.set_halign(Gtk.Align.START)
        label.set_margin_start(4)
        self.get_style_context().add_class('langselector')
        row_box.append(label)
        self.selected_icon = Gtk.Image.new_from_icon_name('object-select-symbolic')
        row_box.append(self.selected_icon)
        self.set_child(row_box)

        self.selected = selected
        self.set_visible(visible)  # This doesn't work.
        row_box.set_visible(visible)  # This does, but it's not what we need.

    @property
    def selected(self):
        return self.selected_icon.get_visible()

    @selected.setter
    def selected(self, value):
        self.selected_icon.set_visible(value)


class LangObject(GObject.Object):
    code = ''
    name = ''
    selected = False
    visible = True

    def __init__(self, code, name, selected=False, visible=True):
        super().__init__()

        self.code = code
        self.name = name
        self.selected = selected
        self.visible = visible
