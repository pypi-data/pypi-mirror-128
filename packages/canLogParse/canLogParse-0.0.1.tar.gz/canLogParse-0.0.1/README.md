# canLogParse
This is a library for importing and parsing data from Kvaser CAN files when you don't have a DBC file. The code should be fairly simple and self-documenting, and all other information should be contained within this file.

## Functions
### `importCanData(rawData, outputFormat="2dArray")`
Imports data from an array of raw packets and returns it as an array of records. The possible formats are `2dArray` (the default), `tupleArray`, and `dict`. This is one of the only two functions you should be using from this library, and documentation on the others is only so that you have an idea of how it works.
####  Output data
The data is structured as follows:
`leadingZero`: The zero at the start of the packet.
`id`: The packet ID.
`dataLength`: The number of data bytes.
`data`: The data bytes in an array.
`T/R`: It is assumed that this is transmit/receive, but so far it has only been observed as `R`.
`timeStamp`: The packet timestamp.

### `importCanLogFile(file, outputFormat="2dArray")`
The same as the above function, but taking the data from a file.

#### Output formats
There are three possible output formats, `2dArray` (the default), `tupleArray`, and `dict`.
`2dArray`: A 2d array, where each inner array represents a packet, and is formatted in the order stated above.
`tupleArray`: The same as `2dArray`, but with tuples instead of inner arrays.
`dict`: An array of dictionaries, with the key names the same as stated above.

### `_formatPacket(leadingZero, id, dataLength, data, tr, timeStamp, outputFormat="2dArray")`
This function takes the given data and formats it in the specified way.

### `_formatPacketList(leadingZero, id, dataLength, data, tr, timeStamp)`, `_formatPacketDict`, and `_formatPacketTuple`
These functions take in the packet data and format it into either a list, a dictionary, or a tuple.

### `_extractDataFromPacket(packet)`
This function takes a packet array and returns the data bytes. It does this by removing all known non-data bytes, which is a terrible way to do it. This function should be updated to extract it using the included `dataLength` byte.
### `_fileToList(file)`
This takes a file name, and returns its rows in a list.

