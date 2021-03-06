/* ************************************************************************
   osparc - the simcore frontend
   https://osparc.io
   Copyright:
     2020 IT'IS Foundation, https://itis.swiss
   License:
     MIT: https://opensource.org/licenses/MIT
   Authors:
     * Odei Maiz (odeimaiz)
************************************************************************ */

/**
 *
 */

qx.Class.define("osparc.desktop.preferences.window.APIKeyBase", {
  extend: qx.ui.window.Window,
  type: "abstract",

  construct: function(caption, infoText) {
    this.base(arguments, caption);

    this.set({
      layout: new qx.ui.layout.VBox(5),
      autoDestroy: true,
      modal: true,
      showMaximize: false,
      showMinimize: false,
      width: 350
    });

    this.__addInfoText(infoText);

    this.center();
  },

  members: {
    __addInfoText: function(infoText) {
      const introLabel = new qx.ui.basic.Label(infoText).set({
        padding: 5,
        rich: true
      });
      this._add(introLabel);
    }
  }
});
