


package body Librflxlang.Lexer_State_Machine is

   Is_Trivia : constant array (Token_Kind) of Boolean := (
      RFLX_Termination => False, RFLX_Lexing_Failure => True, RFLX_Unqualified_Identifier => False, RFLX_Package => False, RFLX_Is => False, RFLX_If => False, RFLX_End => False, RFLX_Null => False, RFLX_Type => False, RFLX_Range => False, RFLX_With => False, RFLX_Mod => False, RFLX_Message => False, RFLX_Then => False, RFLX_Sequence => False, RFLX_Of => False, RFLX_In => False, RFLX_Not => False, RFLX_New => False, RFLX_For => False, RFLX_When => False, RFLX_Where => False, RFLX_Use => False, RFLX_All => False, RFLX_Some => False, RFLX_Generic => False, RFLX_Session => False, RFLX_Begin => False, RFLX_Private => False, RFLX_Return => False, RFLX_Function => False, RFLX_State => False, RFLX_Transition => False, RFLX_Goto => False, RFLX_Exception => False, RFLX_Renames => False, RFLX_Channel => False, RFLX_Readable => False, RFLX_Writable => False, RFLX_Desc => False, RFLX_Append => False, RFLX_Extend => False, RFLX_Read => False, RFLX_Write => False, RFLX_Reset => False, RFLX_First => False, RFLX_Size => False, RFLX_Last => False, RFLX_Checksum => False, RFLX_Valid_Checksum => False, RFLX_Has_Data => False, RFLX_Head => False, RFLX_Opaque => False, RFLX_Present => False, RFLX_Valid => False, RFLX_Initial => False, RFLX_Final => False, RFLX_Dot => False, RFLX_Comma => False, RFLX_Double_Dot => False, RFLX_Tick => False, RFLX_Hash => False, RFLX_Minus => False, RFLX_Arrow => False, RFLX_L_Par => False, RFLX_R_Par => False, RFLX_L_Brack => False, RFLX_R_Brack => False, RFLX_Exp => False, RFLX_Mul => False, RFLX_Div => False, RFLX_Add => False, RFLX_Sub => False, RFLX_Eq => False, RFLX_Neq => False, RFLX_Leq => False, RFLX_Lt => False, RFLX_Le => False, RFLX_Gt => False, RFLX_Ge => False, RFLX_And => False, RFLX_Or => False, RFLX_Ampersand => False, RFLX_Semicolon => False, RFLX_Double_Colon => False, RFLX_Assignment => False, RFLX_Colon => False, RFLX_Comment => True, RFLX_Numeral => False, RFLX_String_Literal => False
   );

   type Character_Range is record
      First, Last : Character_Type;
   end record;

   type Character_Range_Array is array (Positive range <>) of Character_Range;
   --  Sorted list of dijoint character ranges

   pragma Warnings (Off, "referenced");
   function Contains
     (Char : Character_Type; Ranges : Character_Range_Array) return Boolean;
   --  Return whether Char is included in the given ranges
   pragma Warnings (On, "referenced");

   ----------------
   -- Initialize --
   ----------------

   procedure Initialize
     (Self        : out Lexer_State;
      Input       : Text_Access;
      Input_First : Positive;
      Input_Last  : Natural) is
   begin
      Self.Input := Input;
      Self.Input_First := Input_First;
      Self.Input_Last := Input_Last;
      Self.Has_Next := True;
      Self.Last_Token := (Kind       => RFLX_Termination,
                          Text_First => Input_First,
                          Text_Last  => Input_First - 1);
      Self.Last_Token_Kind := RFLX_Termination;
   end Initialize;

   ----------------
   -- Last_Token --
   ----------------

   function Last_Token (Self : Lexer_State) return Lexed_Token is
   begin
      return Self.Last_Token;
   end Last_Token;

   --------------
   -- Has_Next --
   --------------

   function Has_Next (Self : Lexer_State) return Boolean is
   begin
      return Self.Has_Next;
   end Has_Next;

   --------------
   -- Contains --
   --------------

   function Contains
     (Char : Character_Type; Ranges : Character_Range_Array) return Boolean
   is
      Low  : Natural := Ranges'First;
      High : Natural := Ranges'Last;
   begin
      while Low <= High loop
         declare
            Middle : constant Natural := (Low + High) / 2;
            R      : Character_Range renames Ranges (Middle);
         begin
            if Char < R.First then
               High := Middle - 1;
            elsif Char > R.Last then
               Low := Middle + 1;
            else
               return True;
            end if;
         end;
      end loop;
      return False;
   end Contains;



   ----------------
   -- Next_Token --
   ----------------

   procedure Next_Token
     (Self : in out Lexer_State; Token : out Lexed_Token)
   is
      Input : constant Text_Access := Self.Input;

      First_Index : Positive;
      --  Index of the first input character for the token to return

      Index : Positive;
      --  Index for the next input character to be analyzed

      Match_Index : Natural;
      --  If we found a match, index for its last character. Otherwise, zero.

      Match_Ignore : Boolean;
      --  If we found a match, whether we must ignore it and restart the
      --  automaton after its character range.

      Match_Kind : Token_Kind;
      --  If we found a match and it is not ignored, kind for the token to
      --  emit. Meaningless otherwise.
   begin
      First_Index := Self.Last_Token.Text_Last + 1;

      <<Start>>
      Index := First_Index;
      Match_Index := 0;
      Match_Ignore := False;



         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when Character_Type'Val (16#9#) .. Character_Type'Val (16#a#) | Character_Type'Val (16#d#) | ' ' => goto State_1;
               when '"' => goto State_2;
               when '#' => goto State_3;
               when '&' => goto State_4;
               when ''' => goto State_5;
               when '(' => goto State_6;
               when ')' => goto State_7;
               when '*' => goto State_8;
               when '+' => goto State_9;
               when ',' => goto State_10;
               when '-' => goto State_11;
               when '.' => goto State_12;
               when '/' => goto State_13;
               when '0' .. '9' => goto State_14;
               when ':' => goto State_15;
               when ';' => goto State_16;
               when '<' => goto State_17;
               when '=' => goto State_18;
               when '>' => goto State_19;
               when 'A' => goto State_20;
               when 'B' | 'D' .. 'C' | 'E' .. 'D' | 'F' .. 'E' | 'G' | 'I' .. 'H' | 'J' .. 'K' | 'M' .. 'N' | 'P' .. 'O' | 'Q' | 'S' .. 'R' | 'T' .. 'U' | 'W' .. 'V' | 'X' .. 'Z' | 'b' .. 'a' | 'c' .. 'd' | 'f' .. 'e' | 'g' .. 'f' | 'h' | 'j' .. 'l' | 'n' .. 'm' | 'o' .. 'n' | 'p' .. 'o' | 'q' | 's' .. 'r' | 't' .. 's' | 'u' .. 't' | 'v' | 'x' .. 'z' => goto State_21;
               when 'C' => goto State_22;
               when 'D' => goto State_23;
               when 'E' => goto State_24;
               when 'F' => goto State_25;
               when 'H' => goto State_26;
               when 'I' => goto State_27;
               when 'L' => goto State_28;
               when 'O' => goto State_29;
               when 'P' => goto State_30;
               when 'R' => goto State_31;
               when 'S' => goto State_32;
               when 'V' => goto State_33;
               when 'W' => goto State_34;
               when '[' => goto State_35;
               when ']' => goto State_36;
               when 'a' => goto State_37;
               when 'b' => goto State_38;
               when 'e' => goto State_39;
               when 'f' => goto State_40;
               when 'g' => goto State_41;
               when 'i' => goto State_42;
               when 'm' => goto State_43;
               when 'n' => goto State_44;
               when 'o' => goto State_45;
               when 'p' => goto State_46;
               when 'r' => goto State_47;
               when 's' => goto State_48;
               when 't' => goto State_49;
               when 'u' => goto State_50;
               when 'w' => goto State_51;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_1>>

               Match_Index := Index - 1;
               Match_Ignore := True;


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when Character_Type'Val (16#9#) .. Character_Type'Val (16#a#) | Character_Type'Val (16#d#) | ' ' => goto State_52;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_2>>


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when Character_Type'Val (16#0#) .. '!' | '#' .. Character_Type'Val (16#10ffff#) => goto State_53;
               when '"' => goto State_54;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_3>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Hash;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_4>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Ampersand;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_5>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Tick;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_6>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_L_Par;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_7>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_R_Par;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_8>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Mul;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '*' => goto State_55;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_9>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Add;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_10>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Comma;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_11>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Sub;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '-' => goto State_56;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_12>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Dot;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '.' => goto State_57;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_13>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Div;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '=' => goto State_58;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_14>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Numeral;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '#' => goto State_59;
               when '0' .. '9' => goto State_60;
               when '_' => goto State_61;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_15>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Colon;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when ':' => goto State_62;
               when '=' => goto State_63;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_16>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Semicolon;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_17>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Lt;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '=' => goto State_64;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_18>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Eq;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '>' => goto State_65;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_19>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Gt;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '=' => goto State_66;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_20>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'o' | 'q' .. 'z' => goto State_67;
               when 'p' => goto State_68;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_21>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_22>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'g' | 'i' .. 'z' => goto State_67;
               when 'h' => goto State_69;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_23>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_70;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_24>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'w' | 'y' .. 'z' => goto State_67;
               when 'x' => goto State_71;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_25>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_72;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_26>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'a' => goto State_73;
               when 'e' => goto State_74;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_27>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_75;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_28>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_76;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_29>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'o' | 'q' .. 'z' => goto State_67;
               when 'p' => goto State_77;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_30>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'q' | 's' .. 'z' => goto State_67;
               when 'r' => goto State_78;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_31>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_79;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_32>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_80;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_33>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_81;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_34>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'q' | 's' .. 'z' => goto State_67;
               when 'r' => goto State_82;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_35>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_L_Brack;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_36>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_R_Brack;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_37>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'k' | 'm' | 'o' .. 'z' => goto State_67;
               when 'l' => goto State_83;
               when 'n' => goto State_84;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_38>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_85;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_39>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'w' | 'y' .. 'z' => goto State_67;
               when 'n' => goto State_86;
               when 'x' => goto State_87;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_40>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'n' | 'p' .. 't' | 'v' .. 'z' => goto State_67;
               when 'o' => goto State_88;
               when 'u' => goto State_89;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_41>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'n' | 'p' .. 'z' => goto State_67;
               when 'e' => goto State_90;
               when 'o' => goto State_91;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_42>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'e' | 'g' .. 'm' | 'o' .. 'r' | 't' .. 'z' => goto State_67;
               when 'f' => goto State_92;
               when 'n' => goto State_93;
               when 's' => goto State_94;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_43>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'n' | 'p' .. 'z' => goto State_67;
               when 'e' => goto State_95;
               when 'o' => goto State_96;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_44>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'n' | 'p' .. 't' | 'v' .. 'z' => goto State_67;
               when 'e' => goto State_97;
               when 'o' => goto State_98;
               when 'u' => goto State_99;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_45>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'e' | 'g' .. 'q' | 's' .. 'z' => goto State_67;
               when 'f' => goto State_100;
               when 'r' => goto State_101;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_46>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'q' | 's' .. 'z' => goto State_67;
               when 'a' => goto State_102;
               when 'r' => goto State_103;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_47>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'a' => goto State_104;
               when 'e' => goto State_105;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_48>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'n' | 'p' .. 's' | 'u' .. 'z' => goto State_67;
               when 'e' => goto State_106;
               when 'o' => goto State_107;
               when 't' => goto State_108;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_49>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'g' | 'i' .. 'q' | 's' .. 'x' | 'z' => goto State_67;
               when 'h' => goto State_109;
               when 'r' => goto State_110;
               when 'y' => goto State_111;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_50>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'r' | 't' .. 'z' => goto State_67;
               when 's' => goto State_112;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_51>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'g' | 'i' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'h' => goto State_113;
               when 'i' => goto State_114;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_52>>

               Match_Index := Index - 1;
               Match_Ignore := True;


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when Character_Type'Val (16#9#) .. Character_Type'Val (16#a#) | Character_Type'Val (16#d#) | ' ' => goto State_52;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_53>>


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when Character_Type'Val (16#0#) .. '!' | '#' .. Character_Type'Val (16#10ffff#) => goto State_53;
               when '"' => goto State_54;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_54>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_String_Literal;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_55>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Exp;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_56>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Comment;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when Character_Type'Val (16#0#) .. Character_Type'Val (16#9#) | Character_Type'Val (16#b#) .. Character_Type'Val (16#10ffff#) => goto State_115;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_57>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Double_Dot;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_58>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Neq;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_59>>


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'F' => goto State_116;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_60>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Numeral;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '#' => goto State_59;
               when '0' .. '9' => goto State_117;
               when '_' => goto State_61;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_61>>


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' => goto State_118;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_62>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Double_Colon;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_63>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Assignment;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_64>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Le;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_65>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Arrow;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_66>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Ge;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_67>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_68>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'o' | 'q' .. 'z' => goto State_67;
               when 'p' => goto State_119;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_69>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'a' => goto State_120;
               when 'e' => goto State_121;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_70>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'r' | 't' .. 'z' => goto State_67;
               when 's' => goto State_122;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_71>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_123;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_72>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'q' | 's' .. 'z' => goto State_67;
               when 'n' => goto State_124;
               when 'r' => goto State_125;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_73>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'r' | 't' .. 'z' => goto State_67;
               when 's' => goto State_126;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_74>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_127;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_75>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_128;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_76>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'r' | 't' .. 'z' => goto State_67;
               when 's' => goto State_129;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_77>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_130;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_78>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_131;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_79>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'r' | 't' .. 'z' => goto State_67;
               when 'a' => goto State_132;
               when 's' => goto State_133;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_80>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'y' => goto State_67;
               when 'z' => goto State_134;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_81>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'k' | 'm' .. 'z' => goto State_67;
               when 'l' => goto State_135;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_82>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_136;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_83>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'k' | 'm' .. 'z' => goto State_67;
               when 'l' => goto State_137;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_84>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'c' | 'e' .. 'z' => goto State_67;
               when 'd' => goto State_138;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_85>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'f' | 'h' .. 'z' => goto State_67;
               when 'g' => goto State_139;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_86>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'c' | 'e' .. 'z' => goto State_67;
               when 'd' => goto State_140;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_87>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'b' | 'd' .. 'z' => goto State_67;
               when 'c' => goto State_141;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_88>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'q' | 's' .. 'z' => goto State_67;
               when 'r' => goto State_142;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_89>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_143;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_90>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_144;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_91>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_145;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_92>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_If;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_93>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_In;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_94>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Is;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_95>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'r' | 't' .. 'z' => goto State_67;
               when 's' => goto State_146;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_96>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'c' | 'e' .. 'z' => goto State_67;
               when 'd' => goto State_147;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_97>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'v' | 'x' .. 'z' => goto State_67;
               when 'w' => goto State_148;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_98>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_149;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_99>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'k' | 'm' .. 'z' => goto State_67;
               when 'l' => goto State_150;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_100>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Of;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_101>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Or;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_102>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'b' | 'd' .. 'z' => goto State_67;
               when 'c' => goto State_151;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_103>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_152;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_104>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_153;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_105>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 's' | 'u' .. 'z' => goto State_67;
               when 'n' => goto State_154;
               when 't' => goto State_155;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_106>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'p' | 'r' | 't' .. 'z' => goto State_67;
               when 'q' => goto State_156;
               when 's' => goto State_157;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_107>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'l' | 'n' .. 'z' => goto State_67;
               when 'm' => goto State_158;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_108>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_159;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_109>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_160;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_110>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_161;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_111>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'o' | 'q' .. 'z' => goto State_67;
               when 'p' => goto State_162;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_112>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_163;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_113>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_164;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_114>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_165;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_115>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Comment;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when Character_Type'Val (16#0#) .. Character_Type'Val (16#9#) | Character_Type'Val (16#b#) .. Character_Type'Val (16#10ffff#) => goto State_115;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_116>>


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '#' => goto State_166;
               when '0' .. '9' | 'A' .. 'F' => goto State_167;
               when '_' => goto State_168;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_117>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Numeral;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '#' => goto State_59;
               when '0' .. '9' => goto State_117;
               when '_' => goto State_61;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_118>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Numeral;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' => goto State_169;
               when '_' => goto State_61;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_119>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_170;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_120>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_171;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_121>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'b' | 'd' .. 'z' => goto State_67;
               when 'c' => goto State_172;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_122>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'b' | 'd' .. 'z' => goto State_67;
               when 'c' => goto State_173;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_123>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_174;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_124>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_175;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_125>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'r' | 't' .. 'z' => goto State_67;
               when 's' => goto State_176;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_126>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | 'a' .. 'z' => goto State_67;
               when '_' => goto State_177;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_127>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'c' | 'e' .. 'z' => goto State_67;
               when 'd' => goto State_178;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_128>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_179;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_129>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_180;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_130>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'p' | 'r' .. 'z' => goto State_67;
               when 'q' => goto State_181;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_131>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'r' | 't' .. 'z' => goto State_67;
               when 's' => goto State_182;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_132>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'c' | 'e' .. 'z' => goto State_67;
               when 'd' => goto State_183;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_133>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_184;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_134>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_185;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_135>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_186;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_136>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_187;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_137>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_All;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_138>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_And;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_139>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_188;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_140>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_End;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_141>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_189;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_142>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_For;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_143>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'b' | 'd' .. 'z' => goto State_67;
               when 'c' => goto State_190;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_144>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_191;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_145>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'n' | 'p' .. 'z' => goto State_67;
               when 'o' => goto State_192;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_146>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'r' | 't' .. 'z' => goto State_67;
               when 's' => goto State_193;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_147>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Mod;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_148>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_New;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_149>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Not;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_150>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'k' | 'm' .. 'z' => goto State_67;
               when 'l' => goto State_194;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_151>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'j' | 'l' .. 'z' => goto State_67;
               when 'k' => goto State_195;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_152>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'u' | 'w' .. 'z' => goto State_67;
               when 'v' => goto State_196;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_153>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'f' | 'h' .. 'z' => goto State_67;
               when 'g' => goto State_197;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_154>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_198;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_155>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 't' | 'v' .. 'z' => goto State_67;
               when 'u' => goto State_199;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_156>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 't' | 'v' .. 'z' => goto State_67;
               when 'u' => goto State_200;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_157>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'r' | 't' .. 'z' => goto State_67;
               when 's' => goto State_201;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_158>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_202;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_159>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_203;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_160>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_204;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_161>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_205;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_162>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_206;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_163>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Use;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_164>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'q' | 's' .. 'z' => goto State_67;
               when 'r' => goto State_207;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_165>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'g' | 'i' .. 'z' => goto State_67;
               when 'h' => goto State_208;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_166>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Numeral;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         Index := Index + 1;
         goto Stop;

            <<State_167>>


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '#' => goto State_166;
               when '0' .. '9' | 'A' .. 'F' => goto State_209;
               when '_' => goto State_168;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_168>>


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'F' => goto State_210;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_169>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Numeral;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' => goto State_169;
               when '_' => goto State_61;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_170>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_211;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_171>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_212;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_172>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'j' | 'l' .. 'z' => goto State_67;
               when 'k' => goto State_213;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_173>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Desc;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_174>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_214;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_175>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'k' | 'm' .. 'z' => goto State_67;
               when 'l' => goto State_215;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_176>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_216;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_177>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'C' | 'E' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;
               when 'D' => goto State_217;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_178>>

               case Self.Last_Token_Kind is
                     when RFLX_Tick =>
                        Match_Kind := RFLX_Head;
                        Match_Index := Index - 1 - 0;
                     when others =>
                        Match_Kind := RFLX_Unqualified_Identifier;
                        Match_Index := Index - 1 - 0;
               end case;


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_179>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_218;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_180>>

               case Self.Last_Token_Kind is
                     when RFLX_Tick =>
                        Match_Kind := RFLX_Last;
                        Match_Index := Index - 1 - 0;
                     when others =>
                        Match_Kind := RFLX_Unqualified_Identifier;
                        Match_Index := Index - 1 - 0;
               end case;


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_181>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 't' | 'v' .. 'z' => goto State_67;
               when 'u' => goto State_219;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_182>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_220;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_183>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Read;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_221;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_184>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_222;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_185>>

               case Self.Last_Token_Kind is
                     when RFLX_Tick =>
                        Match_Kind := RFLX_Size;
                        Match_Index := Index - 1 - 0;
                     when others =>
                        Match_Kind := RFLX_Unqualified_Identifier;
                        Match_Index := Index - 1 - 0;
               end case;


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_186>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'c' | 'e' .. 'z' => goto State_67;
               when 'd' => goto State_223;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_187>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'a' => goto State_224;
               when 'e' => goto State_225;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_188>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_226;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_189>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'o' | 'q' .. 'z' => goto State_67;
               when 'p' => goto State_227;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_190>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_228;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_191>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'q' | 's' .. 'z' => goto State_67;
               when 'r' => goto State_229;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_192>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Goto;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_193>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_230;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_194>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Null;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_195>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_231;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_196>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_232;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_197>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_233;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_198>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'l' | 'n' .. 'z' => goto State_67;
               when 'm' => goto State_234;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_199>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'q' | 's' .. 'z' => goto State_67;
               when 'r' => goto State_235;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_200>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_236;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_201>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_237;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_202>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Some;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_203>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_238;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_204>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Then;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_205>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'r' | 't' .. 'z' => goto State_67;
               when 's' => goto State_239;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_206>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Type;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_207>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_240;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_208>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_With;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_209>>


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '#' => goto State_166;
               when '0' .. '9' | 'A' .. 'F' => goto State_209;
               when '_' => goto State_168;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_210>>


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '#' => goto State_166;
               when '0' .. '9' | 'A' .. 'F' => goto State_241;
               when '_' => goto State_168;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_211>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'c' | 'e' .. 'z' => goto State_67;
               when 'd' => goto State_242;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_212>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_243;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_213>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'r' | 't' .. 'z' => goto State_67;
               when 's' => goto State_244;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_214>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'c' | 'e' .. 'z' => goto State_67;
               when 'd' => goto State_245;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_215>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Final;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_216>>

               case Self.Last_Token_Kind is
                     when RFLX_Tick =>
                        Match_Kind := RFLX_First;
                        Match_Index := Index - 1 - 0;
                     when others =>
                        Match_Kind := RFLX_Unqualified_Identifier;
                        Match_Index := Index - 1 - 0;
               end case;


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_217>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_246;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_218>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_247;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_219>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_248;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_220>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_249;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_221>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' | 'c' .. 'z' => goto State_67;
               when 'b' => goto State_250;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_222>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Reset;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_223>>

               case Self.Last_Token_Kind is
                     when RFLX_Tick =>
                        Match_Kind := RFLX_Valid;
                        Match_Index := Index - 1 - 0;
                     when others =>
                        Match_Kind := RFLX_Unqualified_Identifier;
                        Match_Index := Index - 1 - 0;
               end case;


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | 'a' .. 'z' => goto State_67;
               when '_' => goto State_251;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_224>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' | 'c' .. 'z' => goto State_67;
               when 'b' => goto State_252;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_225>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Write;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_226>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Begin;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_227>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_253;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_228>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_254;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_229>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_255;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_230>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'f' | 'h' .. 'z' => goto State_67;
               when 'g' => goto State_256;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_231>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'f' | 'h' .. 'z' => goto State_67;
               when 'g' => goto State_257;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_232>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_258;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_233>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Range;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_234>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_259;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_235>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_260;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_236>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_261;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_237>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'n' | 'p' .. 'z' => goto State_67;
               when 'o' => goto State_262;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_238>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_State;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_239>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_263;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_240>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Where;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_241>>


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '#' => goto State_166;
               when '0' .. '9' | 'A' .. 'F' => goto State_241;
               when '_' => goto State_168;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_242>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Append;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_243>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'k' | 'm' .. 'z' => goto State_67;
               when 'l' => goto State_264;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_244>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 't' | 'v' .. 'z' => goto State_67;
               when 'u' => goto State_265;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_245>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Extend;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_246>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_266;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_247>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'k' | 'm' .. 'z' => goto State_67;
               when 'l' => goto State_267;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_248>>

               case Self.Last_Token_Kind is
                     when RFLX_Tick =>
                        Match_Kind := RFLX_Opaque;
                        Match_Index := Index - 1 - 0;
                     when others =>
                        Match_Kind := RFLX_Unqualified_Identifier;
                        Match_Index := Index - 1 - 0;
               end case;


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_249>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_268;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_250>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'k' | 'm' .. 'z' => goto State_67;
               when 'l' => goto State_269;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_251>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'B' | 'D' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;
               when 'C' => goto State_270;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_252>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'k' | 'm' .. 'z' => goto State_67;
               when 'l' => goto State_271;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_253>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_272;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_254>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'n' | 'p' .. 'z' => goto State_67;
               when 'o' => goto State_273;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_255>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'b' | 'd' .. 'z' => goto State_67;
               when 'c' => goto State_274;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_256>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_275;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_257>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_276;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_258>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_277;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_259>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'r' | 't' .. 'z' => goto State_67;
               when 's' => goto State_278;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_260>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Return;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_261>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'b' | 'd' .. 'z' => goto State_67;
               when 'c' => goto State_279;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_262>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_280;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_263>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 's' | 'u' .. 'z' => goto State_67;
               when 't' => goto State_281;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_264>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Channel;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_265>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'l' | 'n' .. 'z' => goto State_67;
               when 'm' => goto State_282;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_266>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'b' .. 'z' => goto State_67;
               when 'a' => goto State_283;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_267>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Initial;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_268>>

               case Self.Last_Token_Kind is
                     when RFLX_Tick =>
                        Match_Kind := RFLX_Present;
                        Match_Index := Index - 1 - 0;
                     when others =>
                        Match_Kind := RFLX_Unqualified_Identifier;
                        Match_Index := Index - 1 - 0;
               end case;


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_269>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_284;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_270>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'g' | 'i' .. 'z' => goto State_67;
               when 'h' => goto State_285;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_271>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_286;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_272>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'n' | 'p' .. 'z' => goto State_67;
               when 'o' => goto State_287;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_273>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_288;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_274>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Generic;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_275>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Message;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_276>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Package;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_277>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Private;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_278>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Renames;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_279>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_289;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_280>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Session;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_281>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'h' | 'j' .. 'z' => goto State_67;
               when 'i' => goto State_290;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_282>>

               case Self.Last_Token_Kind is
                     when RFLX_With =>
                        Match_Kind := RFLX_Checksum;
                        Match_Index := Index - 1 - 0;
                     when others =>
                        Match_Kind := RFLX_Unqualified_Identifier;
                        Match_Index := Index - 1 - 0;
               end case;


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_283>>

               case Self.Last_Token_Kind is
                     when RFLX_Tick =>
                        Match_Kind := RFLX_Has_Data;
                        Match_Index := Index - 1 - 0;
                     when others =>
                        Match_Kind := RFLX_Unqualified_Identifier;
                        Match_Index := Index - 1 - 0;
               end case;


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_284>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Readable;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_285>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'd' | 'f' .. 'z' => goto State_67;
               when 'e' => goto State_291;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_286>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Writable;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_287>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_292;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_288>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Function;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_289>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Sequence;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_290>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'n' | 'p' .. 'z' => goto State_67;
               when 'o' => goto State_293;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_291>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'b' | 'd' .. 'z' => goto State_67;
               when 'c' => goto State_294;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_292>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Exception;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_293>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'm' | 'o' .. 'z' => goto State_67;
               when 'n' => goto State_295;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_294>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'j' | 'l' .. 'z' => goto State_67;
               when 'k' => goto State_296;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_295>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Transition;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_296>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'r' | 't' .. 'z' => goto State_67;
               when 's' => goto State_297;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_297>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 't' | 'v' .. 'z' => goto State_67;
               when 'u' => goto State_298;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_298>>

               Match_Index := Index - 1;
               Match_Kind := RFLX_Unqualified_Identifier;

         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'l' | 'n' .. 'z' => goto State_67;
               when 'm' => goto State_299;

            when others =>

               goto Stop;
            end case;
         end;

            <<State_299>>

               case Self.Last_Token_Kind is
                     when RFLX_Tick =>
                        Match_Kind := RFLX_Valid_Checksum;
                        Match_Index := Index - 1 - 0;
                     when others =>
                        Match_Kind := RFLX_Unqualified_Identifier;
                        Match_Index := Index - 1 - 0;
               end case;


         if Index > Self.Input_Last then
            goto Stop;
         end if;

         declare
            Input_Char : constant Character_Type := Input (Index);
         begin
            Index := Index + 1;

            case Input_Char is
               when '0' .. '9' | 'A' .. 'Z' | '_' | 'a' .. 'z' => goto State_67;

            when others =>

               goto Stop;
            end case;
         end;


      <<Stop>>
      --  We end up here as soon as the currently analyzed character was not
      --  accepted by any transitions from the current state. Two cases from
      --  there:

      if Match_Index = 0 then
         --  We haven't found a match. Just create an error token and plan to
         --  start a new token at the next character.
         if Index > Self.Input_Last then
            Token := (RFLX_Termination, Index, Index - 1);
            Self.Has_Next := False;
         else
            Token := (RFLX_Lexing_Failure, First_Index, First_Index);
         end if;

      elsif Match_Ignore then
         --  We found a match. It must be ignored: resume lexing to start right
         --  after the matched text.
         First_Index := Match_Index + 1;
         goto Start;

      else
         --  We found a match for which we must emit a token
         Token := (Match_Kind, First_Index, Match_Index);
      end if;

      Self.Last_Token := Token;
      if not Is_Trivia (Token.Kind) then
         Self.Last_Token_Kind := Token.Kind;
      end if;
   end Next_Token;

end Librflxlang.Lexer_State_Machine;
