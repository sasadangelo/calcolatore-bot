# Page - Generic Streaamlit Page
#
# This class is a generic streamlit page. All the application pages will derive from this class.
#
# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo sasadangelo@gmail.com
#
# This file is part of the BOT Calculator project.
#
# SPDX-License-Identifier: MIT

# This class represents a generic application page. All the application pages must
# derive from this class.
class Page:
    def render(self):
        raise NotImplementedError("Subclasses must implement the render method")