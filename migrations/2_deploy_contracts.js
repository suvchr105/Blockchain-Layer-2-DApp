const Layer2DApp = artifacts.require("Layer2DApp");

module.exports = function(deployer) {
  deployer.deploy(Layer2DApp);
};
