class CountryCellRenderer {
  init(params) {
    this.eGui = document.createElement('img');
    this.eGui.alt = params.data;

    const context = params.context;
    this.eGui.src =
      context.base64flags[context.countryCodes[params.data.country]];
  }

  getGui() {
    return this.eGui;
  }

  refresh() {
    return false;
  }
}
