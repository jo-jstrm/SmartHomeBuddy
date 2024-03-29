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

goog.exportSymbol("proto.SmartHomeBuddy.IdentifyRequest", null, global);
goog.exportSymbol("proto.SmartHomeBuddy.IdentifyResponse", null, global);
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
proto.SmartHomeBuddy.IdentifyRequest = function (opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.SmartHomeBuddy.IdentifyRequest, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.SmartHomeBuddy.IdentifyRequest.displayName =
    "proto.SmartHomeBuddy.IdentifyRequest";
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
proto.SmartHomeBuddy.IdentifyResponse = function (opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.SmartHomeBuddy.IdentifyResponse, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.SmartHomeBuddy.IdentifyResponse.displayName =
    "proto.SmartHomeBuddy.IdentifyResponse";
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
  proto.SmartHomeBuddy.IdentifyRequest.prototype.toObject = function (
    opt_includeInstance
  ) {
    return proto.SmartHomeBuddy.IdentifyRequest.toObject(
      opt_includeInstance,
      this
    );
  };

  /**
   * Static version of the {@see toObject} method.
   * @param {boolean|undefined} includeInstance Deprecated. Whether to include
   *     the JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @param {!proto.SmartHomeBuddy.IdentifyRequest} msg The msg instance to transform.
   * @return {!Object}
   * @suppress {unusedLocalVariables} f is only used for nested messages
   */
  proto.SmartHomeBuddy.IdentifyRequest.toObject = function (
    includeInstance,
    msg
  ) {
    var f,
      obj = {
        classifierModel: jspb.Message.getFieldWithDefault(msg, 1, ""),
        measurement: jspb.Message.getFieldWithDefault(msg, 2, ""),
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
 * @return {!proto.SmartHomeBuddy.IdentifyRequest}
 */
proto.SmartHomeBuddy.IdentifyRequest.deserializeBinary = function (bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.SmartHomeBuddy.IdentifyRequest();
  return proto.SmartHomeBuddy.IdentifyRequest.deserializeBinaryFromReader(
    msg,
    reader
  );
};

/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.SmartHomeBuddy.IdentifyRequest} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.SmartHomeBuddy.IdentifyRequest}
 */
proto.SmartHomeBuddy.IdentifyRequest.deserializeBinaryFromReader = function (
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
        msg.setClassifierModel(value);
        break;
      case 2:
        var value = /** @type {string} */ (reader.readString());
        msg.setMeasurement(value);
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
proto.SmartHomeBuddy.IdentifyRequest.prototype.serializeBinary = function () {
  var writer = new jspb.BinaryWriter();
  proto.SmartHomeBuddy.IdentifyRequest.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};

/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.SmartHomeBuddy.IdentifyRequest} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.SmartHomeBuddy.IdentifyRequest.serializeBinaryToWriter = function (
  message,
  writer
) {
  var f = undefined;
  f = message.getClassifierModel();
  if (f.length > 0) {
    writer.writeString(1, f);
  }
  f = message.getMeasurement();
  if (f.length > 0) {
    writer.writeString(2, f);
  }
};

/**
 * optional string classifier_model = 1;
 * @return {string}
 */
proto.SmartHomeBuddy.IdentifyRequest.prototype.getClassifierModel =
  function () {
    return /** @type {string} */ (
      jspb.Message.getFieldWithDefault(this, 1, "")
    );
  };

/**
 * @param {string} value
 * @return {!proto.SmartHomeBuddy.IdentifyRequest} returns this
 */
proto.SmartHomeBuddy.IdentifyRequest.prototype.setClassifierModel = function (
  value
) {
  return jspb.Message.setProto3StringField(this, 1, value);
};

/**
 * optional string measurement = 2;
 * @return {string}
 */
proto.SmartHomeBuddy.IdentifyRequest.prototype.getMeasurement = function () {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};

/**
 * @param {string} value
 * @return {!proto.SmartHomeBuddy.IdentifyRequest} returns this
 */
proto.SmartHomeBuddy.IdentifyRequest.prototype.setMeasurement = function (
  value
) {
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
  proto.SmartHomeBuddy.IdentifyResponse.prototype.toObject = function (
    opt_includeInstance
  ) {
    return proto.SmartHomeBuddy.IdentifyResponse.toObject(
      opt_includeInstance,
      this
    );
  };

  /**
   * Static version of the {@see toObject} method.
   * @param {boolean|undefined} includeInstance Deprecated. Whether to include
   *     the JSPB instance for transitional soy proto support:
   *     http://goto/soy-param-migration
   * @param {!proto.SmartHomeBuddy.IdentifyResponse} msg The msg instance to transform.
   * @return {!Object}
   * @suppress {unusedLocalVariables} f is only used for nested messages
   */
  proto.SmartHomeBuddy.IdentifyResponse.toObject = function (
    includeInstance,
    msg
  ) {
    var f,
      obj = {};

    if (includeInstance) {
      obj.$jspbMessageInstance = msg;
    }
    return obj;
  };
}

/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.SmartHomeBuddy.IdentifyResponse}
 */
proto.SmartHomeBuddy.IdentifyResponse.deserializeBinary = function (bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.SmartHomeBuddy.IdentifyResponse();
  return proto.SmartHomeBuddy.IdentifyResponse.deserializeBinaryFromReader(
    msg,
    reader
  );
};

/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.SmartHomeBuddy.IdentifyResponse} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.SmartHomeBuddy.IdentifyResponse}
 */
proto.SmartHomeBuddy.IdentifyResponse.deserializeBinaryFromReader = function (
  msg,
  reader
) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
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
proto.SmartHomeBuddy.IdentifyResponse.prototype.serializeBinary = function () {
  var writer = new jspb.BinaryWriter();
  proto.SmartHomeBuddy.IdentifyResponse.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};

/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.SmartHomeBuddy.IdentifyResponse} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.SmartHomeBuddy.IdentifyResponse.serializeBinaryToWriter = function (
  message,
  writer
) {
  var f = undefined;
};

goog.object.extend(exports, proto.SmartHomeBuddy);
