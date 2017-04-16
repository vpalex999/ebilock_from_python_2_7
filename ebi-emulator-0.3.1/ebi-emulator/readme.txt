For start EbiLock emulator IUT version, make config.json file, and run command: 

java -jar ebi-emulator-0.3.1.jar emulator_config.json

java -jar file.jar [config.json]

How to run without console:
Windows:
javaw -jar ebi-emulator-0.3.1.jar emulator_config.json

Linux:
java -jar ebi-emulator-0.3.1.jar emulator_config.json > /dev/null &

===========================
JSON example: 

{
  "port1": 9090,
  "port2": 9091,
  "package_delay": 600,
  "package_delay_answer_1": 140,
  "package_delay_answer_2": 140,
  "cases": [
    {
      "Telegrams": [
        { "ocAddr": "0x3257", "TelegramRules": [""], "Zones": [0,1,2,3] },
        { "ocAddr": "0x3258", "TelegramRules": [""], "Zones": [0,1,2,3] }
      ],
      "Repeat": 0,
      "PackageRules": ["ONLY_FIRST_CLIENT", "PUSH_BY_ONE_BYTE_SLP", "ADD_GARBAGE_BEFORE_HDLC", "ADD_GARBAGE_AFTER_HDLC", ""]
    },
    {
      "Telegrams": [
        { "ocAddr": "0x3257", "TelegramRules": [""], "Zones": [3,2,1,0] },
        { "ocAddr": "0x3258", "TelegramRules": [""], "Zones": [0,1,2,3] }
      ],
      "Repeat": 1,
      "PackageRules": ["ONLY_FIRST_CLIENT", "SET_NULLBYTE_NOT_NULL"]
    },
    {
      "Telegrams": [
        { "ocAddr": "0x3257", "TelegramRules": [""], "Zones": [3,2,1,0] },
        { "ocAddr": "0x3258", "TelegramRules": [""], "Zones": [3,2,1,0] }
      ],
      "Repeat": 5,
      "PackageRules": [""]
    },
    {
      "Telegrams": [
        { "ocAddr": "0x3257", "TelegramRules": ["SET_WRONG_A_CRC8"], "Zones": [0,1,2,3] },
        { "ocAddr": "0x3258", "TelegramRules": [""], "Zones": [0,1,2,3] }
      ],
      "Repeat": 0,
      "PackageRules": [""]
    },
    {
      "Telegrams": [
        { "ocAddr": "0x3257", "TelegramRules": [""], "Zones": [0,1,2,3] },
        { "ocAddr": "0x3258", "TelegramRules": [""], "Zones": [0,1,2,3] }
      ],
      "Repeat": 0,
      "PackageRules": ["SEND_EMPTY_ORDER"]
    }
  ]
}

=========================== 
port1 	- 	Listen first port from 80-65535
port2 	- 	Listen second port from 80-65535
package_delay -	Delay between packages, ms
package_delay_answer_1 - Wait first answer time, ms
package_delay_answer_2 - Wait second answer time, ms
ocAddr	-	address for Object Controller in hex format
Zones 	-	zone statuses: 0-error, 1-clear, 2-work, 3-train
Repeat	-	how many times repeat this package

Zones numeration starts from left to right: "Zones": [0,1,2,3] == [zone1,zone2,zone3,zone4,zone5,...,zone36]

===========================
Telegram Rules:
    SET_WRONG_A_CRC8	- Set wrong CRC8 for telegram A
    SET_WRONG_B_CRC8	- Set wrong CRC8 for telegram B
    SET_CYCLE_AB_PLUS1	- Set CYCLE A+1 B-1
    SET_ML_A_0		- Set telegram A LENGTH as 0 (ML=0x05)
    SET_ML_B_0		- Set telegram B LENGTH as 0 (ML=0x05)
    SET_NULL_DATA_A	- Set empty DATA for telegram A
    SET_NULL_DATA_B	- Set empty DATA for telegram B
    SET_ML_A_NULL	- Set telegram A LENGTH as NULL (ML=0x00)
    SET_ML_B_NULL	- Set telegram B LENGTH as NULL (ML=0x00)
    SET_CO_A_STATUS	- Set TYPE telegram A = status
    SET_CO_B_STATUS	- Set TYPE telegram B = status
    SET_DOUBLE_TELEGRAM_AB	- Set double telegrams AB
    SET_DOUBLE_TELEGRAM_AB_V2	- Set double telegrams AB Version2

===========================
Package Rules:
    /** For ALL rules and ALL clients, for Developers only */
    PUSH_BY_ONE_BYTE_SLP	- Push data in the socket by one byte using Thead.sleep - it make more parts, but less stable
    PUSH_BY_ONE_BYTE_SCH	- Push data in the socket by one byte using scheduleWithFixedDelay - it make little parts but more stable
    /** For ALL rules and ALL clients, for Developers only */

    /** */
    ONLY_FIRST_CLIENT		- Use all rules only for first port client
    ONLY_SECOND_CLIENT		- Use all rules only for second port client
    /** */

    ADD_GARBAGE_BEFORE_HDLC	- Add 5 random bytes before HDLC
    ADD_GARBAGE_AFTER_HDLC	- Add 5 random bytes after HDLC

    /** not changed by other rules */
    SEND_STATUS_TELEGRAM		- Send_STATUS_telegram(!!!)
    SEND_EMPTY_ORDER			- Send empty odrder, without body
    SEND_GARBAGE_HDLC			- Send garbage instead of normal data
    SEND_GARBAGE_HDLC_SIZED		- Send garbage sized by _LIMIT instead of normal data
    SEND_GARBAGE_OVERSIZED_HDLC		- Send oversized(_LIMIT+1) garbage HDLC
    SEND_GARBAGE_DOUBLESIZED_HDLC	- Send DOUBLESIZED garbage HDLC
    SEND_GARBAGE_THIRDSIZED_HDLC	- Send THIRDSIZED garbage HDLC
    SEND_GARBAGE_FOURTHSIZED_HDLC	- Send FOURTHSIZED garbage HDLC
    SEND_HDLC_DOUBLESIZED		- Send DOUBLESIZED hdlc
    SEND_HDLC_THIRDSIZED		- Send THIRDSIZED hdlc
    SEND_HDLC_FOURTHSIZED		- Send FOURTHSIZED hdlc
    SEND_TWO_HDLC_IN_PACKAGE		- Send TWO hdlc telegrams with NOT increased counters in 1 package
    SEND_FOUR_HDLC_IN_PACKAGE		- Send FOUR hdlc telegrams with NOT increased counters in 1 package
    SEND_TWO_HDLC_IN_PACKAGE_COUNTERS	- Send TWO hdlc telegrams WITH increased counters in 1 package
    /** not changed by other rules */

    SET_PACKAGE_WRONG_CRC16	- Set wrong_CRC16_sum
    SET_PACKAGE_FROM_CLIENT	- Set package_FROM_client
    SET_PACKAGE_TO_IPU		- Set package_TO_ipu
    SET_PACKAGE_TYPE_2		- Set package_TYPE_as Order
    SET_PACKAGE_TYPE_3		- Set package_TYPE_as Status
    SET_PACKAGE_TYPE_4		- Set package_TYPE_as Empty order
    SET_PACKAGE_TYPE_5		- Set package_TYPE_as Data between OCs
    SET_PACKAGE_WRONG_LENGTH	- Set package_LENGTH_not as body length
    SET_PACKAGE_NULL_LENGTH	- Set package_LENGTH_as 0x00
    SET_PACKAGE_NULL_BODY	- Set_BODY_as Empty
    SET_NULLBYTE_NOT_NULL	- Set NULL byte(0x00) as not NULL(0x01)

    /** TM = telegrams */
    SET_TM_WRONG_CYCLE_A	- Set wrong_CYCLE_telegram A
    SET_TM_WRONG_CYCLE_B	- Set wrong_CYCLE_telegram B
    SET_TM_CYCLE_AB_PLUS1	- Set_CYCLE_A+1,B-1
    SET_TM_CYCLE_AB_PLUS2	- Set_CYCLE_A+2,B-2
    SET_TM_WRONG_HEADER_BLOCK_SIZE	- 
    SET_TM_NULL_HEADER_BLOCK_SIZE	- 
    SET_TM_EMPTY_BODY_SIZE	- 
    SET_TM_DOUBLE_BODY		- Repeat body twice, with same data and counters
    /** TM = telegrams */



