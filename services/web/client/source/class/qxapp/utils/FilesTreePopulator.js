/* eslint no-warning-comments: "off" */

qx.Class.define("qxapp.utils.FilesTreePopulator", {
  extend: qx.core.Object,

  construct: function(tree) {
    this.__tree = tree;
  },

  members: {
    __tree: null,

    populateNodeFiles: function(nodeId) {
      const treeName = "Node files";
      this.__resetTree(treeName);

      let store = qxapp.data.Store.getInstance();
      store.addListenerOnce("NodeFiles", e => {
        const files = e.getData();
        const newChildren = qxapp.data.Converters.fromDSMToVirtualTreeModel(files);
        this.__addTreeData(newChildren);
      }, this);
      store.getNodeFiles(nodeId);
    },

    populateMyDocuments: function() {
      const treeName = "My Documents";
      this.__resetTree(treeName);

      let locationsAdded = [];
      let store = qxapp.data.Store.getInstance();
      store.addListenerOnce("MyDocuments", e => {
        const {
          location,
          files
        } = e.getData();
        if (!locationsAdded.includes(location)) {
          locationsAdded.push(location);
          const newChildren = qxapp.data.Converters.fromDSMToVirtualTreeModel(files);
          this.__addTreeData(newChildren);
        }
      }, this);
      store.getMyDocuments();

      /*
      store.addListenerOnce("FakeFiles", e => {
        const files = e.getData();
        const newChildren = qxapp.data.Converters.fromDSMToVirtualTreeModel(files);
        this.__addTreeData(newChildren);
      }, this);
      store.getFakeFiles();
      */
    },

    __resetTree: function(treeName) {
      // FIXME: It is not reseting the model
      this.__tree.resetModel();
      let data = {
        label: treeName,
        fileId: null,
        location: null,
        path: null,
        children: []
      };
      let emptyModel = qx.data.marshal.Json.createModel(data, true);
      this.__tree.setModel(emptyModel);
      this.__tree.setDelegate({
        createItem: () => new qxapp.component.widget.FileTreeItem(),
        bindItem: (c, item, id) => {
          c.bindDefaultProperties(item, id);
          c.bindProperty("fileId", "fileId", null, item, id);
          c.bindProperty("location", "location", null, item, id);
          c.bindProperty("path", "path", null, item, id);
          c.bindProperty("size", "size", null, item, id);
        }
      });
    },

    __addTreeData: function(data) {
      let newModelToAdd = qx.data.marshal.Json.createModel(data, true);
      let currentModel = this.__tree.getModel();
      currentModel.getChildren().append(newModelToAdd);
      this.__tree.setModel(currentModel);
    }
  }
});