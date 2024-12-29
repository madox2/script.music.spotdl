.PHONY: install clean zip

# Variables
ADDON_NAME = script.music.spotdl
PYTHON = python3
PIP = pip3

# Get version from addon.xml
VERSION = $(shell grep -oP '(?<=version=")[^"]+' addon.xml)

install:
	$(PIP) install -r requirements.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	rm -f $(ADDON_NAME)-*.zip

zip: clean
	zip -r $(ADDON_NAME)-$(VERSION).zip . \
		-x "*.git*" \
		-x "*.pyc" \
		-x "*.pyo" \
		-x "*.pyd" \
		-x "__pycache__/*" \
		-x "Makefile" \
		-x "*.zip"

dev-install: zip
	@echo "Installing addon to Kodi development environment..."
	@if [ -d "$$HOME/.kodi/addons/$(ADDON_NAME)" ]; then \
		rm -rf "$$HOME/.kodi/addons/$(ADDON_NAME)"; \
	fi
	@mkdir -p "$$HOME/.kodi/addons"
	@ln -s "$(PWD)" "$$HOME/.kodi/addons/$(ADDON_NAME)"
	@echo "Addon installed successfully!"

help:
	@echo "Available commands:"
	@echo "  make install     - Install Python dependencies"
	@echo "  make clean      - Remove Python cache files and build artifacts"
	@echo "  make zip        - Create a release zip file"
	@echo "  make dev-install - Install addon to local Kodi environment"
	@echo "  make help       - Show this help message"