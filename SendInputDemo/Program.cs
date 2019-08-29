using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

class Program
{
    const int INPUT_MOUSE = 0;
    const int INPUT_KEYBOARD = 1;
    const int INPUT_HARDWARE = 2;
    const uint KEYEVENTF_EXTENDEDKEY = 0x0001;
    const uint KEYEVENTF_KEYUP = 0x0002;
    const uint KEYEVENTF_UNICODE = 0x0004;
    const uint KEYEVENTF_SCANCODE = 0x0008;

    struct INPUT
    {
        public int type;
        public InputUnion u;
    }

    [StructLayout(LayoutKind.Explicit)]
    struct InputUnion
    {
        [FieldOffset(0)]
        public MOUSEINPUT mi;
        [FieldOffset(0)]
        public KEYBDINPUT ki;
        [FieldOffset(0)]
        public HARDWAREINPUT hi;
    }

    [StructLayout(LayoutKind.Sequential)]
    struct MOUSEINPUT
    {
        public int dx;
        public int dy;
        public uint mouseData;
        public uint dwFlags;
        public uint time;
        public IntPtr dwExtraInfo;
    }

    [StructLayout(LayoutKind.Sequential)]
    struct KEYBDINPUT
    {
        public ushort wVk;
        public ushort wScan;
        public uint dwFlags;
        public uint time;
        public IntPtr dwExtraInfo;
    }

    [StructLayout(LayoutKind.Sequential)]
    struct HARDWAREINPUT
    {
        public uint uMsg;
        public ushort wParamL;
        public ushort wParamH;
    }

    [DllImport("user32.dll")]
    static extern IntPtr GetMessageExtraInfo();

    [DllImport("user32.dll", SetLastError = true)]
    static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);

    static void SendKey(char key)
    {
        // convert a normal key to the scan code
        // https://gist.github.com/tracend/912308
        ushort scanKey = 0;
        switch (key)
        {
            case '5':
                scanKey = 0x06;
                break;
            case '1':
                scanKey = 0x02;
                break;
            case 'l':
                scanKey = 0xCB;
                break;
            case 'r':
                scanKey = 0xCD;
                break;
            case 'u':
                scanKey = 0xC8;
                break;
            case 'd':
                scanKey = 0xD0;
                break;
            default:
                throw new NotImplementedException();
        }

        INPUT[] keyPress = new INPUT[]
        {
            new INPUT
            {
                type = INPUT_KEYBOARD,
                u = new InputUnion
                {
                    ki = new KEYBDINPUT
                    {
                        wVk = 0,
                        wScan = scanKey,
                        dwFlags = KEYEVENTF_SCANCODE,
                        dwExtraInfo = IntPtr.Zero,
                    }
                }
            },
        };

        // Key DOWN
        if (SendInput((uint)keyPress.Length, keyPress, Marshal.SizeOf(typeof(INPUT))) == 0)
        {
            Console.WriteLine("SendInput failed with code: " + Marshal.GetLastWin32Error().ToString());
        }
        Thread.Sleep(50); // MAME Emulator requires this

        // key UP
        keyPress[0].u.ki.dwFlags = KEYEVENTF_KEYUP | KEYEVENTF_SCANCODE;
        if (SendInput((uint)keyPress.Length, keyPress, Marshal.SizeOf(typeof(INPUT))) == 0)
        {
            Console.WriteLine("SendInput failed with code: " + Marshal.GetLastWin32Error().ToString());
        }
        Thread.Sleep(50); // MAME Emulator requires this
    }

    static void Main(string[] args)
    {
        Console.WriteLine("TODO: Automatically set focus to MAME Emulator");
        Console.WriteLine("Waiting for you to do that...");
        Thread.Sleep(5000);
        Console.WriteLine("Sending keys...");

        // add a credit
        SendKey('5');

        // player 1
        SendKey('1');

        // wait for the game to start up...
        Thread.Sleep(2000);

        // left, then right, then left, ... :)
        for (int i = 0; i < 50; i++)
        {
            SendKey('l');
            SendKey('r');
        }
    }
}
