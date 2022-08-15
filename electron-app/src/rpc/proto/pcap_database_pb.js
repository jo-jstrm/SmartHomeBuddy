// source: pcap_database.proto
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

goog.exportSymbol("proto.SmartHomeBuddy.DbLoadRequest", null, global);
goog.exportSymbol("proto.SmartHomeBuddy.DbLoadResponse", null, global);
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
proto.SmartHomeBuddy.DbLoadRequest = function (opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.SmartHomeBuddy.DbLoadRequest, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.SmartHomeBuddy.DbLoadRequest.displayName =
    "proto.SmartHomeBuddy.DbLoadRequest";
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
proto.SmartHomeBuddy.DbLoadResponse = function (opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.SmartHomeBuddy.DbLoadResponse, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.SmartHomeBuddy.DbLoadResponse.displayName =
    "proto.SmartHomeBuddy.DbLoadResponse";
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
  proto.SmartHomeBuddy.DbLoadRequest.prototype.toObject = function (
    opt_includeInstance
  ) {
    return proto.SmartHomeBuddy.DbLoadRequest.toObject(
      opt_includeInstance,
      this
    );
  };

  /**
   * Static version of the {@see toObject} method.
   * @param {boolean|undefined} includeInstance Deprecated. Whether to include
   *     the JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @param {!proto.SmartHomeBuddy.DbLoadRequest} msg The msg instance to transform.
   * @return {!Object}
   * @suppress {unusedLocalVariables} f is only used for nested messages
   */
  proto.SmartHomeBuddy.DbLoadRequest.toObject = function (
    includeInstance,
    msg
  ) {
    var f,
      obj = {
        filePath: jspb.Message.getFieldWithDefault(msg, 1, ""),
        fileType: jspb.Message.getFieldWithDefault(msg, 2, ""),
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
 * @return {!proto.SmartHomeBuddy.DbLoadRequest}
 */
proto.SmartHomeBuddy.DbLoadRequest.deserializeBinary = function (bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.SmartHomeBuddy.DbLoadRequest();
  return proto.SmartHomeBuddy.DbLoadRequest.deserializeBinaryFromReader(
    msg,
    reader
  );
};

/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.SmartHomeBuddy.DbLoadRequest} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.SmartHomeBuddy.DbLoadRequest}
 */
proto.SmartHomeBuddy.DbLoadRequest.deserializeBinaryFromReader = function (
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
        msg.setFilePath(value);
        break;
      case 2:
        var value = /** @type {string} */ (reader.readString());
        msg.setFileType(value);
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
proto.SmartHomeBuddy.DbLoadRequest.prototype.serializeBinary = function () {
  var writer = new jspb.BinaryWriter();
  proto.SmartHomeBuddy.DbLoadRequest.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};

/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.SmartHomeBuddy.DbLoadRequest} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.SmartHomeBuddy.DbLoadRequest.serializeBinaryToWriter = function (
  message,
  writer
) {
  var f = undefined;
  f = message.getFilePath();
  if (f.length > 0) {
    writer.writeString(1, f);
  }
  f = message.getFileType();
  if (f.length > 0) {
    writer.writeString(2, f);
  }
};

/**
 * optional string file_path = 1;
 * @return {string}
 */
proto.SmartHomeBuddy.DbLoadRequest.prototype.getFilePath = function () {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};

/**
 * @param {string} value
 * @return {!proto.SmartHomeBuddy.DbLoadRequest} returns this
 */
proto.SmartHomeBuddy.DbLoadRequest.prototype.setFilePath = function (value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};

/**
 * optional string file_type = 2;
 * @return {string}
 */
proto.SmartHomeBuddy.DbLoadRequest.prototype.getFileType = function () {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};

/**
 * @param {string} value
 * @return {!proto.SmartHomeBuddy.DbLoadRequest} returns this
 */
proto.SmartHomeBuddy.DbLoadRequest.prototype.setFileType = function (value) {
  return jspb.Message.setProto3StringField(this, 2, value);
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
  proto.SmartHomeBuddy.DbLoadResponse.prototype.toObject = function (
    opt_includeInstance
  ) {
    return proto.SmartHomeBuddy.DbLoadResponse.toObject(
      opt_includeInstance,
      this
    );
  };

  /**
   * Static version of the {@see toObject} method.
   * @param {boolean|undefined} includeInstance Deprecated. Whether to include
   *     the JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @param {!proto.SmartHomeBuddy.DbLoadResponse} msg The msg instance to transform.
   * @return {!Object}
   * @suppress {unusedLocalVariables} f is only used for nested messages
   */
  proto.SmartHomeBuddy.DbLoadResponse.toObject = function (
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
 * @return {!proto.SmartHomeBuddy.DbLoadResponse}
 */
proto.SmartHomeBuddy.DbLoadResponse.deserializeBinary = function (bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.SmartHomeBuddy.DbLoadResponse();
  return proto.SmartHomeBuddy.DbLoadResponse.deserializeBinaryFromReader(
    msg,
    reader
  );
};

/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.SmartHomeBuddy.DbLoadResponse} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.SmartHomeBuddy.DbLoadResponse}
 */
proto.SmartHomeBuddy.DbLoadResponse.deserializeBinaryFromReader = function (
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
proto.SmartHomeBuddy.DbLoadResponse.prototype.serializeBinary = function () {
  var writer = new jspb.BinaryWriter();
  proto.SmartHomeBuddy.DbLoadResponse.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};

/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.SmartHomeBuddy.DbLoadResponse} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.SmartHomeBuddy.DbLoadResponse.serializeBinaryToWriter = function (
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
proto.SmartHomeBuddy.DbLoadResponse.prototype.getIsDone = function () {
  return /** @type {boolean} */ (
    jspb.Message.getBooleanFieldWithDefault(this, 1, false)
  );
};

/**
 * @param {boolean} value
 * @return {!proto.SmartHomeBuddy.DbLoadResponse} returns this
 */
proto.SmartHomeBuddy.DbLoadResponse.prototype.setIsDone = function (value) {
  return jspb.Message.setProto3BooleanField(this, 1, value);
};

goog.object.extend(exports, proto.SmartHomeBuddy);