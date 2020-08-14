function Decoder(bytes, port) {

  // Based on https://stackoverflow.com/a/37471538 by Ilya Bursov
  function bytesToFloat(bytes) {
    // JavaScript bitwise operators yield a 32 bits integer, not a float.
    // Assume LSB (least significant byte first).
    var bits = bytes[3]<<24 | bytes[2]<<16 | bytes[1]<<8 | bytes[0];
    var sign = (bits>>>31 === 0) ? 1.0 : -1.0;
    var e = bits>>>23 & 0xff;
    var m = (e === 0) ? (bits & 0x7fffff)<<1 : (bits & 0x7fffff) | 0x800000;
    var f = sign * m * Math.pow(2, e - 150);
    return f;
  } 

  function byteToSignedInt(byte) {
	  return byte>127 ? (256 - byte) * -1 : byte;
  }  

  if (port === 1) {
     // Test data BE9A96C2DDB22042
	 return {
		// Take bytes 0 to 4 (not including), and convert to float:
		lng : bytesToFloat(bytes.slice(0, 4)),
		lat : bytesToFloat(bytes.slice(4, 8))
		}
	}
	
  if (port === 2) {
     // Test data E946027E
	 return {
		celsius : byteToSignedInt(bytes[0]) ,
		humidity : bytes[1],
		waterlevel : bytes[2],
		voltage : bytes[3] /10,
		}
	}

}