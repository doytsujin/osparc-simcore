/* ************************************************************************

   osparc - the simcore frontend

   https://osparc.io

   Copyright:
     2019 IT'IS Foundation, https://itis.swiss

   License:
     MIT: https://opensource.org/licenses/MIT

   Authors:
     * Odei Maiz (odeimaiz)

************************************************************************ */

/**
 * Widget that provides access to the data belonging to the active user.
 * - On the left side: myData FilesTree with the FileLabelWithActions
 * - On the right side: a pie chart reflecting the data resources consumed (hidden until there is real info)
 *
 * *Example*
 *
 * Here is a little example of how to use the widget.
 *
 * <pre class='javascript'>
 *   let dataManager = new osparc.dashboard.DataBrowser();
 *   this.getRoot().add(dataManager);
 * </pre>
 */

qx.Class.define("osparc.dashboard.DataBrowser", {
  extend: qx.ui.core.Widget,

  construct: function() {
    this.base(arguments);

    const prjBrowserLayout = new qx.ui.layout.VBox(10);
    this._setLayout(prjBrowserLayout);

    this.__createDataManagerLayout();

    this.addListener("appear", () => {
      this.__initResources(null);
    }, this);
  },

  members: {
    __filesTree: null,
    __selectedFileLayout: null,
    __pieChart: null,

    __initResources: function(locationId) {
      this.__filesTree.populateTree(locationId);
    },

    __createDataManagerLayout: function() {
      const dataManagerMainLayout = new qx.ui.container.Composite(new qx.ui.layout.VBox(10)).set({
        marginTop: 20
      });

      const treeLayout = this.__createTreeLayout();
      dataManagerMainLayout.add(treeLayout, {
        flex: 1
      });

      this._add(dataManagerMainLayout, {
        flex: 1
      });
    },

    __createTreeLayout: function() {
      const treeLayout = new qx.ui.container.Composite(new qx.ui.layout.VBox(10));

      // button for refetching data
      const reloadBtn = new qx.ui.form.Button().set({
        label: this.tr("Reload"),
        font: "text-14",
        icon: "@FontAwesome5Solid/sync-alt/14",
        allowGrowX: false
      });
      reloadBtn.addListener("execute", function() {
        this.__filesTree.resetCache();
        this.__initResources(null);
      }, this);
      treeLayout.add(reloadBtn);

      const filesTree = this.__filesTree = new osparc.file.FilesTree().set({
        dragMechnism: true,
        dropMechnism: true
      });
      filesTree.addListener("selectionChanged", () => {
        this.__selectionChanged();
      }, this);
      filesTree.addListener("fileCopied", e => {
        if (e) {
          this.__initResources(null);
        }
      }, this);
      treeLayout.add(filesTree, {
        flex: 1
      });

      const actionsToolbar = this.__createActionsToolbar();
      treeLayout.add(actionsToolbar);

      return treeLayout;
    },

    __createActionsToolbar: function() {
      const actionsToolbar = new qx.ui.toolbar.ToolBar();
      const fileActions = new qx.ui.toolbar.Part();
      const addFile = new qx.ui.toolbar.Part();
      actionsToolbar.add(fileActions);
      actionsToolbar.addSpacer();
      actionsToolbar.add(addFile);

      const selectedFileLayout = this.__selectedFileLayout = new osparc.file.FileLabelWithActions();
      selectedFileLayout.addListener("fileDeleted", e => {
        const fileMetadata = e.getData();
        this.__initResources(fileMetadata["locationId"]);
      }, this);
      fileActions.add(selectedFileLayout);

      return actionsToolbar;
    },

    __selectionChanged: function() {
      this.__filesTree.resetSelection();
      const selectionData = this.__filesTree.getSelectedFile();
      if (selectionData) {
        this.__selectedFileLayout.itemSelected(selectionData["selectedItem"], selectionData["isFile"]);
      }
    },

    __reloadChartData: function(pathId) {
      if (this.__pieChart) {
        const dataInfo = this.__getDataInfo(pathId);
        const ids = dataInfo["ids"];
        const labels = dataInfo["labels"];
        const values = dataInfo["values"];
        const tooltips = dataInfo["tooltips"];
        const title = dataInfo["title"];
        this.__pieChart.setData(ids, labels, values, tooltips, title);
      }
    },

    __getDataInfo: function(pathId) {
      const context = pathId || "/";
      const children = this.__filesTree.getModel().getChildren();

      let data = {
        "ids": [],
        "labels": [],
        "values": [],
        "tooltips": [],
        "title": context
      };
      if (pathId === undefined) {
        data["ids"].push("FreeSpaceId");
        data["labels"].push("Free space");
        const value = (Math.floor(Math.random()*1000000)+1);
        data["values"].push(value);
        data["tooltips"].push(osparc.utils.Utils.bytesToSize(value));
      }
      for (let i=0; i<children.length; i++) {
        const child = children.toArray()[i];
        data["ids"].push(child.getLabel());
        data["labels"].push(child.getLabel());
        const value2 = (Math.floor(Math.random()*1000000)+1);
        data["values"].push(value2);
        data["tooltips"].push(osparc.utils.Utils.bytesToSize(value2));
      }
      return data;
    }
  }
});
