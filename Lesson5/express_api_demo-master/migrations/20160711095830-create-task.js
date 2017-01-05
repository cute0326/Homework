// Generated by CoffeeScript 1.10.0
(function() {
  'use strict';
  module.exports = {
    up: function(queryInterface, Sequelize) {
      return queryInterface.createTable('tasks', {
        id: {
          allowNull: false,
          autoIncrement: true,
          primaryKey: true,
          type: Sequelize.INTEGER
        },
        title: {
          type: Sequelize.STRING
        },
        desc: {
          type: Sequelize.STRING
        },
        done: {
          type: Sequelize.BOOLEAN,
          defaultValue: false
        },
        createdAt: {
          allowNull: false,
          type: Sequelize.DATE
        },
        updatedAt: {
          allowNull: false,
          type: Sequelize.DATE
        }
      });
    },
    down: function(queryInterface, Sequelize) {
      return queryInterface.dropTable('Tasks');
    }
  };

}).call(this);