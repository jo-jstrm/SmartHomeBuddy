// source: devices_database.proto
/**
 * @fileoverview
 * @enhanceable
 * @suppress {missingRequire} reports error on implicit type usages.
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!
/* eslint-disable */
// @ts-nocheck

var jspb = require("google-protobuf");
var goog = jspb;
var global = Function("return this")();

goog.exportSymbol("proto.SmartHomeBuddy.ClassifyRequest", null, global);
goog.exportSymbol("proto.SmartHomeBuddy.ClassifyResponse", null, global);
goog.exportSymbol("proto.SmartHomeBuddy.Device", null, global);
goog.exportSymbol("proto.SmartHomeBuddy.Devices", null, global);
goog.exportSymbol("proto.SmartHomeBuddy.DevicesRequest", null, global);
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.SmartHomeBuddy.ClassifyRequest = function (opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.SmartHomeBuddy.ClassifyRequest, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.SmartHomeBuddy.ClassifyRequest.displayName =
    "proto.SmartHomeBuddy.ClassifyRequest";
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.SmartHomeBuddy.ClassifyResponse = function (opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.SmartHomeBuddy.ClassifyResponse, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.SmartHomeBuddy.ClassifyResponse.displayName =
    "proto.SmartHomeBuddy.ClassifyResponse";
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.SmartHomeBuddy.DevicesRequest = function (opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.SmartHomeBuddy.DevicesRequest, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.SmartHomeBuddy.DevicesRequest.displayName =
    "proto.SmartHomeBuddy.DevicesRequest";
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.SmartHomeBuddy.Device = function (opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.SmartHomeBuddy.Device, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.SmartHomeBuddy.Device.displayName = "proto.SmartHomeBuddy.Device";
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.SmartHomeBuddy.Devices = function (opt_data) {
  jspb.Message.initialize(
    this,
    opt_data,
    0,
    -1,
    proto.SmartHomeBuddy.Devices.repeatedFields_,
    null
  );
};
goog.inherits(proto.SmartHomeBuddy.Devices, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.SmartHomeBuddy.Devices.displayName = "proto.SmartHomeBuddy.Devices";
}

if (jspb.Message.GENERATE_TO_OBJECT) {
  /**
   * Creates an object representation of this proto.
   * Field names that are reserved in JavaScript and will be renamed to pb_name.
   * Optional fields that are not set will be set to undefined.
   * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
   * For the list of reserved names please see:
   *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
   * @param {boolean=} opt_includeInstance Deprecated. whether to include the
   *     JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @return {!Object}
   */
  proto.SmartHomeBuddy.ClassifyRequest.prototype.toObject = function (
    opt_includeInstance
  ) {
    return proto.SmartHomeBuddy.ClassifyRequest.toObject(
      opt_includeInstance,
      this
    );
  };

  /**
   * Static version of the {@see toObject} method.
   * @param {boolean|undefined} includeInstance Deprecated. Whether to include
   *     the JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @param {!proto.SmartHomeBuddy.ClassifyRequest} msg The msg instance to transform.
   * @return {!Object}
   * @suppress {unusedLocalVariables} f is only used for nested messages
   */
  proto.SmartHomeBuddy.ClassifyRequest.toObject = function (
    includeInstance,
    msg
  ) {
    var f,
      obj = {
        param: jspb.Message.getFieldWithDefault(msg, 1, ""),
      };

    if (includeInstance) {
      obj.$jspbMessageInstance = msg;
    }
    return obj;
  };
}

/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.SmartHomeBuddy.ClassifyRequest}
 */
proto.SmartHomeBuddy.ClassifyRequest.deserializeBinary = function (bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.SmartHomeBuddy.ClassifyRequest();
  return proto.SmartHomeBuddy.ClassifyRequest.deserializeBinaryFromReader(
    msg,
    reader
  );
};

/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.SmartHomeBuddy.ClassifyRequest} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.SmartHomeBuddy.ClassifyRequest}
 */
proto.SmartHomeBuddy.ClassifyRequest.deserializeBinaryFromReader = function (
  msg,
  reader
) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
      case 1:
        var value = /** @type {string} */ (reader.readString());
        msg.setParam(value);
        break;
      default:
        reader.skipField();
        break;
    }
  }
  return msg;
};

/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.SmartHomeBuddy.ClassifyRequest.prototype.serializeBinary = function () {
  var writer = new jspb.BinaryWriter();
  proto.SmartHomeBuddy.ClassifyRequest.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};

/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.SmartHomeBuddy.ClassifyRequest} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.SmartHomeBuddy.ClassifyRequest.serializeBinaryToWriter = function (
  message,
  writer
) {
  var f = undefined;
  f = message.getParam();
  if (f.length > 0) {
    writer.writeString(1, f);
  }
};

/**
 * optional string param = 1;
 * @return {string}
 */
proto.SmartHomeBuddy.ClassifyRequest.prototype.getParam = function () {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};

/**
 * @param {string} value
 * @return {!proto.SmartHomeBuddy.ClassifyRequest} returns this
 */
proto.SmartHomeBuddy.ClassifyRequest.prototype.setParam = function (value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};

if (jspb.Message.GENERATE_TO_OBJECT) {
  /**
   * Creates an object representation of this proto.
   * Field names that are reserved in JavaScript and will be renamed to pb_name.
   * Optional fields that are not set will be set to undefined.
   * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
   * For the list of reserved names please see:
   *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
   * @param {boolean=} opt_includeInstance Deprecated. whether to include the
   *     JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @return {!Object}
   */
  proto.SmartHomeBuddy.ClassifyResponse.prototype.toObject = function (
    opt_includeInstance
  ) {
    return proto.SmartHomeBuddy.ClassifyResponse.toObject(
      opt_includeInstance,
      this
    );
  };

  /**
   * Static version of the {@see toObject} method.
   * @param {boolean|undefined} includeInstance Deprecated. Whether to include
   *     the JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @param {!proto.SmartHomeBuddy.ClassifyResponse} msg The msg instance to transform.
   * @return {!Object}
   * @suppress {unusedLocalVariables} f is only used for nested messages
   */
  proto.SmartHomeBuddy.ClassifyResponse.toObject = function (
    includeInstance,
    msg
  ) {
    var f,
      obj = {
        isDone: jspb.Message.getBooleanFieldWithDefault(msg, 1, false),
      };

    if (includeInstance) {
      obj.$jspbMessageInstance = msg;
    }
    return obj;
  };
}

/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.SmartHomeBuddy.ClassifyResponse}
 */
proto.SmartHomeBuddy.ClassifyResponse.deserializeBinary = function (bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.SmartHomeBuddy.ClassifyResponse();
  return proto.SmartHomeBuddy.ClassifyResponse.deserializeBinaryFromReader(
    msg,
    reader
  );
};

/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.SmartHomeBuddy.ClassifyResponse} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.SmartHomeBuddy.ClassifyResponse}
 */
proto.SmartHomeBuddy.ClassifyResponse.deserializeBinaryFromReader = function (
  msg,
  reader
) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
      case 1:
        var value = /** @type {boolean} */ (reader.readBool());
        msg.setIsDone(value);
        break;
      default:
        reader.skipField();
        break;
    }
  }
  return msg;
};

/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.SmartHomeBuddy.ClassifyResponse.prototype.serializeBinary = function () {
  var writer = new jspb.BinaryWriter();
  proto.SmartHomeBuddy.ClassifyResponse.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};

/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.SmartHomeBuddy.ClassifyResponse} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.SmartHomeBuddy.ClassifyResponse.serializeBinaryToWriter = function (
  message,
  writer
) {
  var f = undefined;
  f = message.getIsDone();
  if (f) {
    writer.writeBool(1, f);
  }
};

/**
 * optional bool is_done = 1;
 * @return {boolean}
 */
proto.SmartHomeBuddy.ClassifyResponse.prototype.getIsDone = function () {
  return /** @type {boolean} */ (
    jspb.Message.getBooleanFieldWithDefault(this, 1, false)
  );
};

/**
 * @param {boolean} value
 * @return {!proto.SmartHomeBuddy.ClassifyResponse} returns this
 */
proto.SmartHomeBuddy.ClassifyResponse.prototype.setIsDone = function (value) {
  return jspb.Message.setProto3BooleanField(this, 1, value);
};

if (jspb.Message.GENERATE_TO_OBJECT) {
  /**
   * Creates an object representation of this proto.
   * Field names that are reserved in JavaScript and will be renamed to pb_name.
   * Optional fields that are not set will be set to undefined.
   * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
   * For the list of reserved names please see:
   *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
   * @param {boolean=} opt_includeInstance Deprecated. whether to include the
   *     JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @return {!Object}
   */
  proto.SmartHomeBuddy.DevicesRequest.prototype.toObject = function (
    opt_includeInstance
  ) {
    return proto.SmartHomeBuddy.DevicesRequest.toObject(
      opt_includeInstance,
      this
    );
  };

  /**
   * Static version of the {@see toObject} method.
   * @param {boolean|undefined} includeInstance Deprecated. Whether to include
   *     the JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @param {!proto.SmartHomeBuddy.DevicesRequest} msg The msg instance to transform.
   * @return {!Object}
   * @suppress {unusedLocalVariables} f is only used for nested messages
   */
  proto.SmartHomeBuddy.DevicesRequest.toObject = function (
    includeInstance,
    msg
  ) {
    var f,
      obj = {
        param: jspb.Message.getFieldWithDefault(msg, 1, ""),
      };

    if (includeInstance) {
      obj.$jspbMessageInstance = msg;
    }
    return obj;
  };
}

/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.SmartHomeBuddy.DevicesRequest}
 */
proto.SmartHomeBuddy.DevicesRequest.deserializeBinary = function (bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.SmartHomeBuddy.DevicesRequest();
  return proto.SmartHomeBuddy.DevicesRequest.deserializeBinaryFromReader(
    msg,
    reader
  );
};

/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.SmartHomeBuddy.DevicesRequest} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.SmartHomeBuddy.DevicesRequest}
 */
proto.SmartHomeBuddy.DevicesRequest.deserializeBinaryFromReader = function (
  msg,
  reader
) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
      case 1:
        var value = /** @type {string} */ (reader.readString());
        msg.setParam(value);
        break;
      default:
        reader.skipField();
        break;
    }
  }
  return msg;
};

/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.SmartHomeBuddy.DevicesRequest.prototype.serializeBinary = function () {
  var writer = new jspb.BinaryWriter();
  proto.SmartHomeBuddy.DevicesRequest.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};

/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.SmartHomeBuddy.DevicesRequest} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.SmartHomeBuddy.DevicesRequest.serializeBinaryToWriter = function (
  message,
  writer
) {
  var f = undefined;
  f = message.getParam();
  if (f.length > 0) {
    writer.writeString(1, f);
  }
};

/**
 * optional string param = 1;
 * @return {string}
 */
proto.SmartHomeBuddy.DevicesRequest.prototype.getParam = function () {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};

/**
 * @param {string} value
 * @return {!proto.SmartHomeBuddy.DevicesRequest} returns this
 */
proto.SmartHomeBuddy.DevicesRequest.prototype.setParam = function (value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};

if (jspb.Message.GENERATE_TO_OBJECT) {
  /**
   * Creates an object representation of this proto.
   * Field names that are reserved in JavaScript and will be renamed to pb_name.
   * Optional fields that are not set will be set to undefined.
   * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
   * For the list of reserved names please see:
   *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
   * @param {boolean=} opt_includeInstance Deprecated. whether to include the
   *     JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @return {!Object}
   */
  proto.SmartHomeBuddy.Device.prototype.toObject = function (
    opt_includeInstance
  ) {
    return proto.SmartHomeBuddy.Device.toObject(opt_includeInstance, this);
  };

  /**
   * Static version of the {@see toObject} method.
   * @param {boolean|undefined} includeInstance Deprecated. Whether to include
   *     the JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @param {!proto.SmartHomeBuddy.Device} msg The msg instance to transform.
   * @return {!Object}
   * @suppress {unusedLocalVariables} f is only used for nested messages
   */
  proto.SmartHomeBuddy.Device.toObject = function (includeInstance, msg) {
    var f,
      obj = {
        name: jspb.Message.getFieldWithDefault(msg, 1, ""),
        macAddress: jspb.Message.getFieldWithDefault(msg, 2, ""),
      };

    if (includeInstance) {
      obj.$jspbMessageInstance = msg;
    }
    return obj;
  };
}

/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.SmartHomeBuddy.Device}
 */
proto.SmartHomeBuddy.Device.deserializeBinary = function (bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.SmartHomeBuddy.Device();
  return proto.SmartHomeBuddy.Device.deserializeBinaryFromReader(msg, reader);
};

/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.SmartHomeBuddy.Device} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.SmartHomeBuddy.Device}
 */
proto.SmartHomeBuddy.Device.deserializeBinaryFromReader = function (
  msg,
  reader
) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
      case 1:
        var value = /** @type {string} */ (reader.readString());
        msg.setName(value);
        break;
      case 2:
        var value = /** @type {string} */ (reader.readString());
        msg.setMacAddress(value);
        break;
      default:
        reader.skipField();
        break;
    }
  }
  return msg;
};

/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.SmartHomeBuddy.Device.prototype.serializeBinary = function () {
  var writer = new jspb.BinaryWriter();
  proto.SmartHomeBuddy.Device.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};

/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.SmartHomeBuddy.Device} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.SmartHomeBuddy.Device.serializeBinaryToWriter = function (
  message,
  writer
) {
  var f = undefined;
  f = message.getName();
  if (f.length > 0) {
    writer.writeString(1, f);
  }
  f = message.getMacAddress();
  if (f.length > 0) {
    writer.writeString(2, f);
  }
};

/**
 * optional string name = 1;
 * @return {string}
 */
proto.SmartHomeBuddy.Device.prototype.getName = function () {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};

/**
 * @param {string} value
 * @return {!proto.SmartHomeBuddy.Device} returns this
 */
proto.SmartHomeBuddy.Device.prototype.setName = function (value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};

/**
 * optional string mac_address = 2;
 * @return {string}
 */
proto.SmartHomeBuddy.Device.prototype.getMacAddress = function () {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};

/**
 * @param {string} value
 * @return {!proto.SmartHomeBuddy.Device} returns this
 */
proto.SmartHomeBuddy.Device.prototype.setMacAddress = function (value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};

/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.SmartHomeBuddy.Devices.repeatedFields_ = [1];

if (jspb.Message.GENERATE_TO_OBJECT) {
  /**
   * Creates an object representation of this proto.
   * Field names that are reserved in JavaScript and will be renamed to pb_name.
   * Optional fields that are not set will be set to undefined.
   * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
   * For the list of reserved names please see:
   *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
   * @param {boolean=} opt_includeInstance Deprecated. whether to include the
   *     JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @return {!Object}
   */
  proto.SmartHomeBuddy.Devices.prototype.toObject = function (
    opt_includeInstance
  ) {
    return proto.SmartHomeBuddy.Devices.toObject(opt_includeInstance, this);
  };

  /**
   * Static version of the {@see toObject} method.
   * @param {boolean|undefined} includeInstance Deprecated. Whether to include
   *     the JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @param {!proto.SmartHomeBuddy.Devices} msg The msg instance to transform.
   * @return {!Object}
   * @suppress {unusedLocalVariables} f is only used for nested messages
   */
  proto.SmartHomeBuddy.Devices.toObject = function (includeInstance, msg) {
    var f,
      obj = {
        devicesList: jspb.Message.toObjectList(
          msg.getDevicesList(),
          proto.SmartHomeBuddy.Device.toObject,
          includeInstance
        ),
      };

    if (includeInstance) {
      obj.$jspbMessageInstance = msg;
    }
    return obj;
  };
}

/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.SmartHomeBuddy.Devices}
 */
proto.SmartHomeBuddy.Devices.deserializeBinary = function (bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.SmartHomeBuddy.Devices();
  return proto.SmartHomeBuddy.Devices.deserializeBinaryFromReader(msg, reader);
};

/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.SmartHomeBuddy.Devices} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.SmartHomeBuddy.Devices}
 */
proto.SmartHomeBuddy.Devices.deserializeBinaryFromReader = function (
  msg,
  reader
) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
      case 1:
        var value = new proto.SmartHomeBuddy.Device();
        reader.readMessage(
          value,
          proto.SmartHomeBuddy.Device.deserializeBinaryFromReader
        );
        msg.addDevices(value);
        break;
      default:
        reader.skipField();
        break;
    }
  }
  return msg;
};

/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.SmartHomeBuddy.Devices.prototype.serializeBinary = function () {
  var writer = new jspb.BinaryWriter();
  proto.SmartHomeBuddy.Devices.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};

/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.SmartHomeBuddy.Devices} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.SmartHomeBuddy.Devices.serializeBinaryToWriter = function (
  message,
  writer
) {
  var f = undefined;
  f = message.getDevicesList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      1,
      f,
      proto.SmartHomeBuddy.Device.serializeBinaryToWriter
    );
  }
};

/**
 * repeated Device devices = 1;
 * @return {!Array<!proto.SmartHomeBuddy.Device>}
 */
proto.SmartHomeBuddy.Devices.prototype.getDevicesList = function () {
  return /** @type{!Array<!proto.SmartHomeBuddy.Device>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.SmartHomeBuddy.Device, 1)
  );
};

/**
 * @param {!Array<!proto.SmartHomeBuddy.Device>} value
 * @return {!proto.SmartHomeBuddy.Devices} returns this
 */
proto.SmartHomeBuddy.Devices.prototype.setDevicesList = function (value) {
  return jspb.Message.setRepeatedWrapperField(this, 1, value);
};

/**
 * @param {!proto.SmartHomeBuddy.Device=} opt_value
 * @param {number=} opt_index
 * @return {!proto.SmartHomeBuddy.Device}
 */
proto.SmartHomeBuddy.Devices.prototype.addDevices = function (
  opt_value,
  opt_index
) {
  return jspb.Message.addToRepeatedWrapperField(
    this,
    1,
    opt_value,
    proto.SmartHomeBuddy.Device,
    opt_index
  );
};

/**
 * Clears the list making it empty but non-null.
 * @return {!proto.SmartHomeBuddy.Devices} returns this
 */
proto.SmartHomeBuddy.Devices.prototype.clearDevicesList = function () {
  return this.setDevicesList([]);
};

goog.object.extend(exports, proto.SmartHomeBuddy);
