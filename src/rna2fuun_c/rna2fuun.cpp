#include "rna2fuun.hpp"

#include <iostream>

const unsigned int w = 600;
const unsigned int h = 600;

const pixel black 	= {0, 0, 0};
const pixel red 	= {255, 0, 0};
const pixel green 	= {0, 255, 0};
const pixel yellow 	= {255, 255, 0};
const pixel blue 	= {0, 0, 255};
const pixel magenta	= {255, 0, 255};
const pixel cyan 	= {0, 255, 255};
const pixel white 	= {255, 255, 255};
const unsigned char transparent = 0;
const unsigned char opaque 		= 255;

const int E = 0;
const int S = 1;
const int W = 2;
const int N = 3;

const int ADDCOLORBLACK = 0;
const int ADDCOLORRED = 1;
const int ADDCOLORGREEN = 2;
const int ADDCOLORYELLOW = 3;
const int ADDCOLORBLUE = 4;
const int ADDCOLORMAGENTA = 5;
const int ADDCOLORCYAN = 6;
const int ADDCOLORWHITE = 7;
const int ADDCOLORTRANSPARENT = 8;
const int ADDCOLOROPAQUE = 9;
const int EMPTYBUCKET = 10;
const int MOVE = 11;
const int TURNCCW = 12;
const int TURNCW = 13;
const int MARK = 14;
const int LINE = 15;
const int TRYFILL = 16;
const int ADDBITMAP = 17;
const int COMPOSE = 18;
const int CLIP = 19;
    
rna2fuun::rna2fuun() 
{ 
	reset();
	m_commands["PIPIIIC"] = ADDCOLORBLACK;
	m_commands["PIPIIIP"] = ADDCOLORRED;
	m_commands["PIPIICC"] = ADDCOLORGREEN;
	m_commands["PIPIICF"] = ADDCOLORYELLOW;
	m_commands["PIPIICP"] = ADDCOLORBLUE;
	m_commands["PIPIIFC"] = ADDCOLORMAGENTA;
	m_commands["PIPIIFF"] = ADDCOLORCYAN;
	m_commands["PIPIIPC"] = ADDCOLORWHITE;
	m_commands["PIPIIPF"] = ADDCOLORTRANSPARENT;
	m_commands["PIPIIPP"] = ADDCOLOROPAQUE;
	m_commands["PIIPICP"] = EMPTYBUCKET;
	m_commands["PIIIIIP"] = MOVE;
	m_commands["PCCCCCP"] = TURNCCW;
	m_commands["PFFFFFP"] = TURNCW;
	m_commands["PCCIFFP"] = MARK;
	m_commands["PFFICCP"] = LINE;
	m_commands["PIIPIIP"] = TRYFILL;
	m_commands["PCCPFFP"] = ADDBITMAP;
	m_commands["PFFPCCP"] = COMPOSE;
	m_commands["PFFICCF"] = CLIP;
}

rna2fuun::~rna2fuun()
{
}

void rna2fuun::reset()
{
	m_cCache = false;
	m_c.r = 0;
	m_c.g = 0;
	m_c.b = 0;
	m_c.a = opaque;
	m_cpCache = false;
	m_cp.r = 0;
	m_cp.g = 0;
	m_cp.b = 0;
	m_cp.a = opaque;
	m_aCache = false;
	m_a = opaque;
    m_x = 0;
    m_y = 0;
    m_mx = 0;
    m_my = 0;
    m_dir = E;
    m_bitmaps.clear();
    addBitmap();
    emptyBucket();
}

void rna2fuun::addColor(const pixel& c)
{
	m_cbucket.push_back(c);
	m_cCache = false;
	m_cpCache = false;
}

void rna2fuun::addAlpha(unsigned char a)
{
	m_abucket.push_back(a);
	m_aCache = false;
	m_cpCache = false;
}

void rna2fuun::emptyBucket()
{
	m_cbucket.clear();
	m_abucket.clear();
	m_cCache = false;
	m_aCache = false;
	m_cpCache = false;
}

pixel rna2fuun::averageColor(unsigned char def) const
{
	if (m_cbucket.empty())
	{
		pixel p;
		p.r = def;
		p.g = def;
		p.b = def;
		p.a = opaque;
		return p;
	}
	else
	{
		if (!m_cCache)
		{
			unsigned int r = 0;
			unsigned int g = 0;
			unsigned int b = 0;
			for (std::vector<pixel>::const_iterator it = m_cbucket.begin(); it != m_cbucket.end(); ++it)
			{
				const pixel& bp = *it;
				r += bp.r;
				g += bp.g;
				b += bp.b;
			}
			size_t sz = m_cbucket.size();
			m_c.r = r / sz;
			m_c.g = g / sz;
			m_c.b = b / sz;
			m_cCache = true;
		}
		return m_c;			
	}
}

unsigned char rna2fuun::averageAlpha(unsigned char def) const
{
	if (m_abucket.empty())
	{
		return def;
	}
	else
	{
		if (!m_aCache)
		{
			unsigned int a = 0;
			for (std::vector<unsigned char>::const_iterator it = m_abucket.begin(); it != m_abucket.end(); ++it)
			{
				a += *it;
			}
			m_a = a / m_abucket.size();
			m_aCache = true;
		}
		return m_a;
	}
}    

const pixel& rna2fuun::currentPixel() const
{
	if (!m_cpCache)
	{
		unsigned char a = averageAlpha(opaque);
		pixel p = averageColor(0);
		m_cp.r = static_cast<unsigned int>(p.r) * static_cast<unsigned int>(a) / 255;		
		m_cp.g = static_cast<unsigned int>(p.g) * static_cast<unsigned int>(a) / 255;		
		m_cp.b = static_cast<unsigned int>(p.b) * static_cast<unsigned int>(a) / 255;
		m_cp.a = a;		
	}
	return m_cp; 
}


void rna2fuun::move()
{
	switch (m_dir)
	{
	case N:
		--m_y;
		if (m_y < 0)
		{
			m_y = h - 1;
		}
		break;
	case E:
		++m_x;
		if (m_x >= w)
		{
			m_x = 0;
		}
		break;
	case S:
		++m_y;
		if (m_y >= h)
		{
			m_y = 0;
		}
		break;
	case W:
		--m_x;
		if (m_x < 0)
		{
			m_x = w - 1;
		}
		break;
	}
}

void rna2fuun::turnCounterClockwise()
{
	--m_dir;
	if (m_dir < 0)
	{
		m_dir = 3;
	}
}

void rna2fuun::turnClockwise()
{
	++m_dir;
	if (m_dir > 3)
	{
		m_dir = 0;
	}
}

void rna2fuun::line()
{
	unsigned int x0 = m_x;
	unsigned int y0 = m_y;
	unsigned int x1 = m_mx;
	unsigned int y1 = m_my;
	
    int deltax = static_cast<int>(x1) - static_cast<int>(x0);
    int deltay = static_cast<int>(y1) - static_cast<int>(y0);
    unsigned int d = std::max(std::abs(deltax), std::abs(deltay));
    
    unsigned int c = 0;
    if ((deltax * deltay) >= 0)
    {
        c = 1;
    }
        
    unsigned int x = x0 * d + (d - c)/2;
    unsigned int y = y0 * d + (d - c)/2;
    pixel cp = currentPixel(); 
    for (unsigned int i = 0; i < d; ++i)
    {
        setPixelVal(x/d, y/d, cp);
        x += deltax;
        y += deltay;
    }
    setPixelVal(x1, y1, cp);
}

void rna2fuun::fill(unsigned int x, unsigned int y, const pixel& oldp, const pixel& newp)
{
	std::vector<std::pair<unsigned int, unsigned int> > stack;
	stack.push_back(std::make_pair(x, y));
    while (!stack.empty())
    {
        std::pair<unsigned int, unsigned int> pos = stack.back();
        stack.pop_back();
        pixel& p = getPixel(pos.first, pos.second);
        if (memcmp(&oldp, &p, sizeof(pixel)) == 0)
        {
        	p = newp;
        	if (pos.second + 1 < h)
        	{
        		stack.push_back(std::make_pair(pos.first, pos.second + 1));
        	}
        	if (pos.first + 1 < w)
        	{
        		stack.push_back(std::make_pair(pos.first + 1, pos.second));
        	}
        	if (pos.second > 1)
        	{
        		stack.push_back(std::make_pair(pos.first, pos.second - 1));
        	}
        	if (pos.first > 1)
        	{
        		stack.push_back(std::make_pair(pos.first - 1, pos.second));
        	}
        }
    }
} 

void rna2fuun::tryfill()
{
	pixel newp = currentPixel();
	pixel oldp = getPixel(m_x, m_y); 
    if (memcmp(&oldp, &newp, sizeof(pixel)) != 0)
    {
        fill(m_x, m_y, oldp, newp);
    }
}

void rna2fuun::addBitmap()
{
	if (m_bitmaps.size() == 10)
	{
		return;
	}
	pixel p;
	p.r = 0;
	p.g = 0;
	p.b = 0;
	p.a = transparent;
	m_bitmaps.insert(m_bitmaps.begin(), std::vector<pixel>(w*h, p));
} 
    
void rna2fuun::compose()
{
    if (m_bitmaps.size() > 1)
    {
        const std::vector<pixel>& bm0 = m_bitmaps[0];
        std::vector<pixel>& bm1 = m_bitmaps[1];
        for (unsigned int i = 0; i < w * h; ++i)
        {
        	const pixel& p0 = bm0[i];
        	pixel& p1 = bm1[i];
            p1.r = p0.r + p1.r * (255 - p0.a) / 255;
            p1.g = p0.g + p1.g * (255 - p0.a) / 255;
            p1.b = p0.b + p1.b * (255 - p0.a) / 255;
            p1.a = p0.a + p1.a * (255 - p0.a) / 255;
        }
        m_bitmaps.erase(m_bitmaps.begin());
    }
}
    
void rna2fuun::clip()
{
    if (m_bitmaps.size() > 1)
    {
        const std::vector<pixel>& bm0 = m_bitmaps[0];
        std::vector<pixel>& bm1 = m_bitmaps[1];
        for (unsigned int i = 0; i < w * h; ++i)
        {
        	const pixel& p0 = bm0[i];
        	pixel& p1 = bm1[i];
            p1.r = p1.r * p0.a / 255;
            p1.g = p1.g * p0.a / 255;
            p1.b = p1.b * p0.a / 255;
            p1.a = p1.a * p0.a / 255;
        }
        m_bitmaps.erase(m_bitmaps.begin());
    }
}    

pixel& rna2fuun::getPixel(unsigned int x, unsigned int y)
{
    return m_bitmaps[0][x + w * y];
}

pixelbuffer rna2fuun::getImage() const 
{ 
	pixelbuffer p;
	p.size = sizeof(pixel) * m_bitmaps[0].size();
	p.data = (const char*)&m_bitmaps[0][0];
	return p;
}


void rna2fuun::mark()
{
	m_mx = m_x;
	m_my = m_y;
}            

void rna2fuun::buildsteps(const std::vector<std::string>& rna)
{
	std::for_each(rna.begin(), rna.end(), std::bind1st(std::mem_fun(&rna2fuun::buildstep), this)); 
}
        
void rna2fuun::buildstep(std::string rna)
{
	std::map<std::string, unsigned int>::const_iterator cit = m_commands.find(rna);
	if (cit != m_commands.end())
	{
		switch (cit->second)
		{
			case ADDCOLORBLACK:
				addColor(black);
				break;
			case ADDCOLORRED:
				addColor(red);
				break;
			case ADDCOLORGREEN:
				addColor(green);
				break;
			case ADDCOLORYELLOW:
				addColor(yellow);
				break;
			case ADDCOLORBLUE:
				addColor(blue);
				break;
			case ADDCOLORMAGENTA:
				addColor(magenta);
				break;
			case ADDCOLORCYAN:
				addColor(cyan);
				break;
			case ADDCOLORWHITE:
				addColor(white);
				break;
			case ADDCOLORTRANSPARENT:
				addAlpha(transparent);
				break;
			case ADDCOLOROPAQUE:
				addAlpha(opaque);
				break;
			case EMPTYBUCKET:
				emptyBucket();
				break;
			case MOVE:
				move();
				break;
			case TURNCCW:
				turnCounterClockwise();
				break;
			case TURNCW:
				turnClockwise();
				break;
			case MARK:
				mark();
				break;
			case LINE:
				line();
				break;
			case TRYFILL:
				tryfill();
				break;
			case ADDBITMAP:
				addBitmap();
				break;
			case COMPOSE:
				compose();
				break;
			case CLIP:
				clip();
				break;
		}
	}
}
